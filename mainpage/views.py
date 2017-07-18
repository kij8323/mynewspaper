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
from investment.models import Investment
from products.models import Products, Application
from updatenew.models import Updatenew
from judgement.models import Instrument
from accounts.models import MyUser

# Create your views here.
ARTICLE_MAINPAGE_TIMERANGE = 8 #首页显示新闻数量
ARTICLE_MAINPAGE_COVER_TIMERANGE = 15	#首页封面文章的发表时间范围
TOPIC_MAINPAGE_COVER_TIMERANGE = 25 #争议话题的发表时间范围
TOPIC_MAINPAGE_TIMERANGE = 15 #热门话题的时间范围
ARTICLE_MAINPAGE_HOT_TIMERANGE = 5 #一周新闻排行的时间范围
COMMENT_MAINPAGE_TIMERANGE = 3 #精彩点评的时间范围
HOTRY_MAINPAGE_RANGE = 3 #首页显示热门试用
ARTICLE_MAINPAGE_HOT_TODAY = 3 #48小时热门新闻


#搜索页面
def index_search(request):
	q = request.GET.get('search_word')
	if q:
		mode = SPH_MATCH_ALL
		host = 'localhost'
		port = 9312
		indexarticle = 'mysql'
		indextopic = 'mysqltopic'
		indexproducts = 'mysqlproducts'
		indexinstrument = 'mysqlinstrument'
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

		
		res4 = cl.Query ( q, indextopic )
		if not res4:
			print 'query failed: %s' % cl.GetLastError()
			sys.exit(1)
		if cl.GetLastWarning():
			print 'WARNING: %s\n' % cl.GetLastWarning()
		index4 = [] #查询结果的id集合
		if res4.has_key('matches'):
			for match in res4['matches']:
				index4.append(match['id']) 
		test4 = Topic.objects.all().filter(id__in = index4).order_by('-id') #获得属于id集合的对象的queryset

		res5 = cl.Query ( q, indexproducts )
		if not res5:
			print 'query failed: %s' % cl.GetLastError()
			sys.exit(1)
		if cl.GetLastWarning():
			print 'WARNING: %s\n' % cl.GetLastWarning()
		index5 = [] #查询结果的id集合
		if res5.has_key('matches'):
			for match in res5['matches']:
				index5.append(match['id']) 
		test5 = Products.objects.all().filter(id__in = index5).order_by('-id') #获得属于id集合的对象的queryset

		res6 = cl.Query ( q, indexinstrument )
		if not res6:
			print 'query failed: %s' % cl.GetLastError()
			sys.exit(1)
		if cl.GetLastWarning():
			print 'WARNING: %s\n' % cl.GetLastWarning()
		index6 = [] #查询结果的id集合
		if res6.has_key('matches'):
			for match in res6['matches']:
				index6.append(match['id'])  
		test6 = Instrument.objects.all().filter(id__in = index6).filter(verify = True).order_by('-id') #获得属于id集合的对象的queryset
		
	
		cache.set("search_word", q)
		# 分页
		paginator = Paginator(test2, 10)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
			pageshow = int(page)#判断是否显示公司
			if pageshow == 1 or pageshow == None:
				firmshow = True
			else:
				firmshow = False
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
			firmshow = True#判断是否显示公司
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
			pageshow = int(page)#判断是否显示公司
			if pageshow == 1 or pageshow == None:
				firmshow = True
			else:
				firmshow = False
		context = {
#			'articlequery' : contacts,
			'search_word' : q,
			'firmshow' : firmshow,
			'test4' : test4,
			'test5' : test5,
#			'test6' : test6,
		}
	else:
		context = {
			'articlequery' : None,
		}
	return render(request, 'index_search.html', context)



#首页
def home(request):
#	coverarticle = Article.objects.all().filter(timestamp__gte=datetime.date.today() - timedelta(days=ARTICLE_MAINPAGE_COVER_TIMERANGE)).filter(cover = True).order_by("-id")[0:3]
#	coverarticle = Article.objects.all().filter(cover = True).order_by("-id")[0:3]
	topic = Topic.objects.all().filter(timestamp__gte=datetime.date.today() - timedelta(days=TOPIC_MAINPAGE_TIMERANGE)).order_by("-readers")[0:5]
	#一个月内，最热文章排序
#	hotnews = Article.objects.all().filter(timestamp__gte=datetime.date.today() - timedelta(days=ARTICLE_MAINPAGE_HOT_TIMERANGE)).order_by("-readers")[0:5]
	nicecomment = Comment.objects.all().filter(timestamp__gte=datetime.date.today() - timedelta(days=COMMENT_MAINPAGE_TIMERANGE)).order_by("-readers")[0:5]
	hotry = Products.objects.filter(verify = True).order_by('-id')[0:HOTRY_MAINPAGE_RANGE]
	coverarticle = Topic.objects.all().filter(cover = True).order_by("-id")[0:3]
	guanggaotopic = Topic.objects.all().filter(guanggao = True).order_by("-id")[0:2]
#	hotnews48 = Article.objects.all().filter(timestamp__gte=datetime.date.today() - timedelta(days=ARTICLE_MAINPAGE_HOT_TODAY)).order_by("-readers")[0]
        scorerank=MyUser.objects.exclude(pk=53).exclude(pk=519).order_by('-score')[0:5]


	groupall = Group.objects.all().exclude(id=11)
	context = {
	'topicquery1' : topic[0:2],
	'topicquery2' : topic[2:5],
#	'hotnews': hotnews,
#	'hotnews48': hotnews48,
#	'hotnewsblock1': hotnews[0:2],
#	'hotnewsblock2': hotnews[2:5],
	'nicecomment': nicecomment,
	'coverarticle': coverarticle,
#	'coverarticle0': coverarticle[0],
#	'coverarticle1': coverarticle[1],
#	'coverarticle2': coverarticle[2],
#	'guanggaotopic': guanggaotopic,
	'guanggaotopic1': guanggaotopic[0],
	'guanggaotopic2': guanggaotopic[1],
	'hotry':hotry,
	'groupall': groupall,
	'scorerank':scorerank,
	}
	return render(request, 'home.html', context)
	#return render(request, 'home.html')

def homepage(request):
	queryset = Updatenew.objects.all().order_by('-id')[0:ARTICLE_MAINPAGE_TIMERANGE]
	topic = Topic.objects.filter(score = True).order_by('-id')[0:ARTICLE_MAINPAGE_TIMERANGE]

#	queryset = Article.objects.all().order_by('-id')[0:ARTICLE_MAINPAGE_TIMERANGE]
	context = {
	'queryset': queryset,
	'topic': topic,
	}
	return render(request, 'homepage.html', context)


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
def moretopichome(request):
	if request.is_ajax():
		request.session['hometopiclen'] = request.POST.get('hometopiclen')
		hometopiclen = int(request.session['hometopiclen'])
		article = Topic.objects.filter(score = True).order_by('-id')

	if article.count() == hometopiclen:
		loadcompleted = '已全部加载完成'
	else:
		loadcompleted = '加载更多'
	data = {
		"loadcompleted": loadcompleted,
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')

#加载更多话题页
def topicpagehome(request):
	if request.session.get('hometopiclen', False):
		hometopiclen = request.session['hometopiclen']

# v1
	hometopic = Topic.objects.filter(score = True).order_by('-id')

	#homearticle = Article.objects.all().order_by('-id')
	hometopiclen = int(hometopiclen)
	topicquery = hometopic[hometopiclen:hometopiclen+5]
	context = {
		"topic": topicquery,
	}
	return render(request, 'topicpagehome.html',  context)




#加载更多文按钮
def morearticlehome(request):
	if request.is_ajax():
		request.session['homearticlelen'] = request.POST.get('homearticlelen')
		homearticlelen = int(request.session['homearticlelen'])
		article = Updatenew.objects.all().order_by('-id')

#		article = Article.objects.all().order_by('-id')
		print request.session['homearticlelen']
	if article.count() == homearticlelen:
		loadcompleted = '已全部加载完成'
	else:
		loadcompleted = '加载更多'
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
#	homearticle = Article.objects.all().order_by('-id')
	homearticle = Updatenew.objects.all().order_by('-id')

	homearticlelen = int(homearticlelen)
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
import xml.etree.ElementTree as ET
from django.utils.encoding import smart_str
import time
# from auto_reply.views import auto_reply_main # 修改这里
# from lxml import etree
def responseMsg(request):  
    rawData = smart_str(request.body)  
    xml = ET.fromstring(rawData)  
    msg = paraseMsgXml(xml)  
    MsgType = msg.get("MsgType")  
    if MsgType == "text":  
        return textMsg(msg)  
    # elif MsgType == "location":  
    #     return locationMsg(msg)  
    else:
	return textMsg(msg)

def paraseMsgXml(rootElem):  
    msg = {}  
    if rootElem.tag == "xml":  
        for child in rootElem:  
            msg[child.tag] = smart_str(child.text)  
    return msg  


def textMsg(msg):  
    ToUserName = msg.get("ToUserName")  
    FromUserName = msg.get("FromUserName")  
    timestamp = msg.get("CreateTime")  
    text = msg.get("MsgType")  
    Content = msg.get("Content")  
  
    replyContent = "接收方帐号："+ToUserName+"\n开发者微信号："+FromUserName+"\nContent："+Content  
    locationXML = """<xml> 
            <ToUserName><![CDATA[%s]]></ToUserName> 
            <FromUserName><![CDATA[%s]]></FromUserName> 
            <CreateTime>%s</CreateTime> 
            <MsgType><![CDATA[text]]></MsgType> 
            <Content><![CDATA[%s]]></Content> 
            </xml>""" %(FromUserName,ToUserName,str(int(time.time())),replyContent)  
    return locationXML  
WEIXIN_TOKEN = 'wutongnews'
#微信验证
@csrf_exempt
def weixinyanzheng(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    if request.method == "GET":
	print 'weixinget`'
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
    elif request.method == "POST":  
	print 'weixin'
        response = HttpResponse(responseMsg(request),content_type="application/xml")  
        return response  
    else:  
        response = None  
        return response  
    # else:
    #     xml_str = smart_str(request.body)
    #     request_xml = etree.fromstring(xml_str)
    #     response_xml = auto_reply_main(request_xml)# 修改这里
    #     return HttpResponse(response_xml)





