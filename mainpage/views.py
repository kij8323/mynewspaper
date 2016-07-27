#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from article.models import Article, Category
from topic.models import Group, Topic
from comment.models import Comment
import datetime
from datetime import timedelta
import json
from django.http import HttpResponse
from sphinxapi import *
import sys
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from company.models import Company
# Create your views here.
ARTICLE_MAINPAGE_TIMERANGE = 15 #首页显示新闻数量
ARTICLE_MAINPAGE_COVER_TIMERANGE = 15	#首页封面文章的发表时间范围
TOPIC_MAINPAGE_COVER_TIMERANGE = 25 #争议话题的发表时间范围
TOPIC_MAINPAGE_TIMERANGE = 15 #热门话题的时间范围
ARTICLE_MAINPAGE_HOT_TIMERANGE = 30 #一周新闻排行的时间范围
COMMENT_MAINPAGE_TIMERANGE = 30 #精彩点评的时间范围

#搜索页面
def index_search(request):
	q = request.GET.get('search_word')
	if q:
		mode = SPH_MATCH_ALL
		host = 'localhost'
		port = 9312
		indexfirm = 'mysqlfirm'
		indexarticle = 'mysql'
		# filtercol = 'group_id'
		# filtervals = []
		# sortby = ''
		# groupby = ''
		# groupsort = '@group desc'
		# limit = 0
		cl = SphinxClient()
		cl.SetServer ( host, port )
		cl.SetWeights ( [100, 1] )
		cl.SetMatchMode ( mode )

		res1 = cl.Query ( q, indexfirm )
		if not res1:
			print 'query failed: %s' % cl.GetLastError()
			sys.exit(1)
		if cl.GetLastWarning():
			print 'WARNING: %s\n' % cl.GetLastWarning()
		index1 = [] #查询结果的id集合
		if res1.has_key('matches'):
			for match in res1['matches']:
				index1.append(match['id'])  
		test1 = Company.objects.all().filter(id__in = index1).filter(verify = True).order_by('-id') #获得属于id集合的对象的queryset
		
		res2 = cl.Query ( q, indexarticle )
		if not res2:
			print 'query failed: %s' % cl.GetLastError()
			sys.exit(1)
		if cl.GetLastWarning():
			print 'WARNING: %s\n' % cl.GetLastWarning()
		index2 = [] #查询结果的id集合
		if res2.has_key('matches'):
			for match in res2['matches']:
				index2.append(match['id']) 
		test2 = Article.objects.all().filter(id__in = index2).order_by('-id') #获得属于id集合的对象的queryset
		
		
		cache.set("search_word", q)
		# 分页
		paginator = Paginator(test2, 10)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
			pageshow = int(page)
			if pageshow == 1 or pageshow == None:
				firmshow = True
			else:
				firmshow = False
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
			firmshow = True
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
			pageshow = int(page)
			if pageshow == 1 or pageshow == None:
				firmshow = True
			else:
				firmshow = False
		context = {
			'articlequery' : contacts,
			'search_word' : q,
			'test1' : test1,
			'firmshow' : firmshow,
		}
	else:
		context = {
			'articlequery' : None,
		}
	return render(request, 'index_search.html', context)


#首页
def home(request):
#	coverarticle = Article.objects.all().filter(timestamp__gte=datetime.date.today() - timedelta(days=ARTICLE_MAINPAGE_COVER_TIMERANGE)).filter(cover = True).order_by("-id")[0:3]
	coverarticle = Article.objects.all().filter(original = True).order_by("-id")[0:3]
	queryset = Article.objects.all().order_by('-id')[0:ARTICLE_MAINPAGE_TIMERANGE]
	topic = Topic.objects.all().filter(timestamp__gte=datetime.date.today() - timedelta(days=TOPIC_MAINPAGE_TIMERANGE)).order_by("-readers")[0:5]
	#一个月内，最热文章排序
	hotnews = Article.objects.all().filter(timestamp__gte=datetime.date.today() - timedelta(days=ARTICLE_MAINPAGE_HOT_TIMERANGE)).order_by("-readers")[0:5]
	nicecomment = Comment.objects.all().filter(timestamp__gte=datetime.date.today() - timedelta(days=COMMENT_MAINPAGE_TIMERANGE)).order_by("-readers")[0:5]
	companyshow = Company.objects.all().filter(verify  = True).order_by("-id")[0:5]
	context = {
	'queryset': queryset,
	'topicquery' : topic,
	'hotnews': hotnews,
	'nicecomment': nicecomment,
	'coverarticle': coverarticle,
	'coverarticle0': coverarticle[0],
	'coverarticle1': coverarticle[1],
	'coverarticle2': coverarticle[2],
	'companyshow': companyshow,	
	}
	return render(request, 'home.html', context)
	#return render(request, 'home.html')

#关于我们页
def aboutus(request):
	return render(request, 'aboutus.html')

#联系我们页
def contactus(request):
	return render(request, 'contactus.html')

#加入我们页
def joinus(request):
	return render(request, 'joinus.html')

#加载更多文按钮
def morearticlehome(request):
	if request.is_ajax():
		request.session['homearticlelen'] = request.POST.get('homearticlelen')
		homearticlelen = int(request.session['homearticlelen'])
		article = Article.objects.all().order_by('-id')
		print request.session['homearticlelen']
	if article.count() == homearticlelen:
		loadcompleted = '已全部加载完成'
	else:
		loadcompleted = '点击加载更多'
		print request.session['homearticlelen']
	print loadcompleted
	data = {
		"loadcompleted": loadcompleted,
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')

#加载更多文章页
def articlepagehome(request):
	if request.session.get('homearticlelen', False):
		homearticlelen = request.session['homearticlelen']
	homearticle = Article.objects.all().order_by('-id')
	homearticlelen = int(homearticlelen)
	print homearticlelen
	articlequery = homearticle[homearticlelen:homearticlelen+5]
	context = {
		"articlequery": articlequery,
	}
	return render(request, 'articlepagehome.html',  context)











import hashlib
import json
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
# from auto_reply.views import auto_reply_main # 修改这里
# from lxml import etree

WEIXIN_TOKEN = 'wutongnews'
#微信验证
#@csrf_exempt
def weixinyanzheng(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin  index")
    # else:
    #     xml_str = smart_str(request.body)
    #     request_xml = etree.fromstring(xml_str)
    #     response_xml = auto_reply_main(request_xml)# 修改这里
    #     return HttpResponse(response_xml)
