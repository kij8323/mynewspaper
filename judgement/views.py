#coding=utf-8
#! /usr/bin/env python 
from django.shortcuts import render
from .models import Instrument, Category, Instrumentusercomment, Instrumentgrade
import json
from django.http import HttpResponse
from django.http import Http404
from comment.models import Comment
import traceback 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from article.form import CommentForm
from article.tasks import instrumentcommentplus, readersin, instancesave
from notifications.atwho import atwho
from django.core.cache import cache
from django.conf import settings
from notifications.signals import notify
from accounts.models import MyUser
from django.core.cache import cache
from sphinxapi import *
from notifications.models import Notification

# Create your views here.
instrument_DETAIL_HOTCOMMENT_READERSRANGE = 5
COMMENT_MAINPAGE_TIMERANGE = 3 #精彩点评的时间范围
from datetime import timedelta
import datetime

def judgement(request):
	nicecomment = Comment.objects.all().exclude(grade = 0).filter(timestamp__gte=datetime.date.today() - timedelta(days=COMMENT_MAINPAGE_TIMERANGE)).order_by("-readers")[0:5]
	context = {
		'nicecomment': nicecomment,
	}
	return render(request, 'instrumentall.html', context)

def newinstru(request):
	id_model= request.POST.get('id_model')
	id_company= request.POST.get('id_company')
	instrument = Instrument(model=id_model,  usercompany=id_company, uper = request.user )
	instrument.save()
	data = {
		"ok": 'ok',
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def instrumentpage(request, category_id):
	category_id = int(category_id)
	if category_id == 0:
		instrumentall = Instrument.objects.all().filter(verify = True).order_by('-id')[0:12]
	elif category_id == 2:
		instrumentall = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')[0:12]
	elif category_id == 3:
		instrumentall = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')[0:12]
	elif category_id == 5:
		instrumentall = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')[0:12]
	elif category_id == 6:
		instrumentall = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')[0:12]
	elif category_id == 7:
		instrumentall = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')[0:12]
	elif category_id == 8:
		instrumentall = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')[0:12]

	context = {
		'instrumentall': instrumentall,
	}
	return render(request, 'instrumentpage.html',  context)



def instrumentindex(request):
	q = request.GET.get('search_word')
	if q:
		mode = SPH_MATCH_ALL
		host = 'localhost'
		port = 9312
		indexinstrument = 'mysqlinstrument'
		cl = SphinxClient()
		cl.SetServer ( host, port )
		cl.SetWeights ( [100, 1] )
		cl.SetMatchMode ( mode )
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
		firmshow = True
		context = {
			'test6' : test6,
			'firmshow': firmshow,
		}
	else:
		context = {
			'articlequery' : None,
		}
	return render(request, 'instrumentindex.html', context)




def instrumentdetail(request, instrument_id):
	instrument = Instrument.objects.get(id = instrument_id)
	instrucate = Instrument.objects.filter(verify = True).filter(category = instrument.category).exclude(id=instrument_id).order_by('-id')[0:3]

	commentorderbyreaders = Comment.objects.filter(instrument=instrument).filter(parent=None).filter(readers__gt=instrument_DETAIL_HOTCOMMENT_READERSRANGE).order_by('-readers')[0:3]
	comment = Comment.objects.filter(instrument=instrument).filter(parent=None).order_by('timestamp')
	#最新话题
	# 分页
	paginator = Paginator(comment, 12)
	page = request.GET.get('page')
	request.session['instrumentcommentpage'] = page
	pagen = 1
	try:
		contacts = paginator.page(page)
		pagen = page
	except PageNotAnInteger:
		contacts = paginator.page(1)
		pagen = 1
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)
		pagen = paginator.num_pages

	ifhotcomment = True;
	if page:
		page = int(page)
		if page > 1:
			ifhotcomment = None;
	else:
		page = 1;

	try:
		instrumentgrade = Instrumentgrade.objects.get(instrument=instrument)
	except:
		instrumentgrade = Instrumentgrade()
		instrumentgrade.instrument = instrument
		instrumentgrade.save()
	context = {
		'instrument': instrument,
		'user': request.user,
		'commentorderbyreaders': commentorderbyreaders,
		'ifhotcomment': ifhotcomment,
		"form": CommentForm,
		"comment": comment,
		'contacts': contacts,
		'page': page,
		"instrumentgrade": instrumentgrade,
		'instrucate': instrucate,
	}
	return render(request, 'instrument_detail.html',  context)



#加载更多评分产品按钮
def moreinstru(request):
	if request.is_ajax():
		request.session['instrulen'] = request.POST.get('instrulen')
		instrulen = int(request.session['instrulen'])

		request.session['cate'] = request.POST.get('cate')
		category_id = int(request.session['cate'])
		if category_id == 0:
			instrument = Instrument.objects.all().filter(verify = True).order_by('-id')
		elif category_id == 2:
			instrument = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')
		elif category_id == 3:
			instrument = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')
		elif category_id == 5:
			instrument = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')
		elif category_id == 6:
			instrument = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')
		elif category_id == 7:
			instrument = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')
		elif category_id == 8:
			instrument = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')


		# print request.session['instrulen']
	if instrument.count() == instrulen:
		loadcompleted = '已全部加载完成'
	else:
		loadcompleted = '加载更多'
	data = {
		"loadcompleted": loadcompleted,
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')

#加载更多评分产品页
def moreinstrupage(request):
	# print 'moreinstrupage'
	if request.session.get('instrulen', False):
		instrulen = request.session['instrulen']
	if request.session.get('cate', False):
		category_id = request.session['cate']
	category_id = int(category_id)
	if category_id == 0:
		instrument = Instrument.objects.all().filter(verify = True).order_by('-id')
	elif category_id == 2:
		instrument = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')
	elif category_id == 3:
		instrument = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')
	elif category_id == 5:
		instrument = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')
	elif category_id == 6:
		instrument = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')
	elif category_id == 7:
		instrument = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')
	elif category_id == 8:
		instrument = Instrument.objects.all().filter(category = category_id).filter(verify = True).order_by('-id')

	instrulen = int(instrulen)
	instrument = instrument[instrulen:instrulen+4]
	context = {
		"instrumentall": instrument,
	}
	return render(request, 'moreinstrupage.html',  context)





#ajax，发送评论,post
def instrumentcomment(request):
	if request.is_ajax() and request.method == 'POST':
		text = request.POST.get('comment')
		instrumentid = request.POST.get('instrumentid')
		grade = int(request.POST.get('grade'))
		instrument = Instrument.objects.get(pk=instrumentid)
		user = request.user
		try:
			c = Comment(user=user, instrument=instrument, text=text, grade = grade)
			c.save()

			userlist = atwho(text = text, sender = user, targetcomment = c, targetproducts = None
							, targetarticle = None, targetopic = None, targetinstrument = instrument)#优先发送@消息
			for item in userlist:
				atwhouser = MyUser.objects.get(username = item)
				test = "@<a href='" +'/user/'+str(atwhouser.id)+'/informations/'+"'>"+atwhouser.username+"</a>"+' '
				test1 = "@<a href='" +'/user/'+str(atwhouser.id)+'/informations/'+"'>"+atwhouser.username+"</a>"+'&nbsp;'
				text = text.replace('@'+item+' ', test);
				text = text.replace('@'+item+'&nbsp;', test1);

			cachekey = "instrument_comment_" + str(instrumentid)
			if cache.get(cachekey) != None:
				cache.incr(cachekey)
			else:
				cache.set(cachekey, instrument.comment_set.count(), settings.CACHE_EXPIRETIME)

			# cachekey = "comment_user_count_" + str(user.id)
			# if cache.get(cachekey) != None:
			# 	cache.incr(cachekey)
			# else:
			# 	usercomnum = Comment.objects.filter(user = user).count()
			# 	cache.set(cachekey,  usercomnum)



			# cachekey = "instrument_comment_noparent_" + str(instrumentid)
			# if cache.get(cachekey) != None:
			# 	cache.incr(cachekey)
			# else:
			# 	cache.set(cachekey, Comment.objects.filter(instrument=instrument).filter(parent = None).count(), settings.CACHE_EXPIRETIME)
			


			try:
				instrumentgrade = Instrumentgrade.objects.get(instrument=instrument)
				instrumentgrade.starall = instrumentgrade.starall+1
				if grade == 2:
					instrumentgrade.star1 = instrumentgrade.star1+1
				elif grade == 4:
					instrumentgrade.star2 = instrumentgrade.star2+1
				elif grade == 6:
					instrumentgrade.star3 = instrumentgrade.star3+1
				elif grade == 8:
					instrumentgrade.star4 = instrumentgrade.star4+1
				elif grade == 10:
					instrumentgrade.star5 = instrumentgrade.star5+1
				else:
					pass
				instrumentgrade.grade = (2*instrumentgrade.star1 + 4*instrumentgrade.star2  + 6*instrumentgrade.star3 + 8*instrumentgrade.star4 + 10*instrumentgrade.star5)/instrumentgrade.starall
				instancesave.delay(instrumentgrade)
			except:
				instrumentgrade = Instrumentgrade()
				instrumentgrade.instrument = instrument
				instrumentgrade.starall = instrumentgrade.starall+1
				if grade == 2:
					instrumentgrade.star1 = instrumentgrade.star1+1
				elif grade == 4:
					instrumentgrade.star2 = instrumentgrade.star2+1
				elif grade == 6:
					instrumentgrade.star3 = instrumentgrade.star3+1
				elif grade == 8:
					instrumentgrade.star4 = instrumentgrade.star4+1
				elif grade == 10:
					instrumentgrade.star5 = instrumentgrade.star5+1
				else:
					pass
				instrumentgrade.grade = (2*instrumentgrade.star1 + 4*instrumentgrade.star2  + 6*instrumentgrade.star3 + 8*instrumentgrade.star4 + 10*instrumentgrade.star5)/instrumentgrade.starall
				instancesave.delay(instrumentgrade)


			instrument.grade = instrumentgrade.grade
			instancesave.delay(instrument)

			try:
				instrumentusercomment = Instrumentusercomment.objects.get(instrument=instrument, user=user)
			except:
				instrumentusercomment = None
			if instrumentusercomment:
				pass
			else:
				instrumentcommentplus.delay(user, instrument, Instrumentusercomment)


			data = {
			"user": user.username,
			"text": text,
			"commentid": c.id,
			}
			json_data = json.dumps(data)
			return HttpResponse(json_data, content_type='application/json')
		except:
			traceback.print_exc()
			raise Http404(traceback)
	else:
		raise Http404






#ajax，发送评论的评论,post
def instrucommentcomment(request):
	if request.is_ajax() and request.method == 'POST':
		text = request.POST.get('comment')
		instrumentid = request.POST.get('instrumentid')
		#parenttext = request.POST.get('parenttext')
		preentid = request.POST.get('preentid')
		instrument = Instrument.objects.get(pk=instrumentid)
		comment = Comment.objects.filter(instrument=instrument)
		targetcomment = Comment.objects.get(pk=preentid)
		user = request.user
		try:
			c = Comment(user=user, instrument=instrument, text=text, parent=targetcomment)
			c.save()

			userlist = atwho(text = text, sender = user, targetcomment = c, targetproducts = None
							, targetarticle = None, targetopic = None, targetinstrument = instrument)#优先发送@消息
			for item in userlist:
				atwhouser = MyUser.objects.get(username = item)
				test = "@<a href='" +'/user/'+str(atwhouser.id)+'/informations/'+"'>"+atwhouser.username+"</a>"+' '
				text = text.replace('@'+item+' ', test);


			if targetcomment.user != user and targetcomment.user.username not in userlist:#再发送回复评论消息
				notify.send(sender=user, target_object= c
						, recipient = targetcomment.user, verb='$'
						, text=text, target_article = None
						, target_products = None
						, target_instrument = instrument)
				cachekey = "user_unread_count" + str(targetcomment.user.id)
				if cache.get(cachekey) != None:
					cache.incr(cachekey)
				else:
					unread = Notification.objects.filter(recipient = targetcomment.user.id).filter(read = False).count()
					cache.set(cachekey,  unread, settings.CACHE_EXPIRETIME)



			# cachekey = "comment_user_count_" + str(user.id)
			# if cache.get(cachekey) != None:
			# 	cache.incr(cachekey)
			# else:
			# 	usercomnum = Comment.objects.filter(user = user).count()
			# 	cache.set(cachekey,  usercomnum)


			cachekey = "instrument_comment_" + str(instrumentid)
			if cache.get(cachekey) != None:
				cache.incr(cachekey)
			else:
				cache.set(cachekey, instrument.comment_set.count(), settings.CACHE_EXPIRETIME)
			readersin(targetcomment)

			data = {
			"user": user.username,
			"text": text,
			"parentcommentext": c.parent.text,
			"parentcommentuser": str(c.parent.user),
			"commentid":c.id,
			}
			json_data = json.dumps(data)
			return HttpResponse(json_data, content_type='application/json')
		except:
			traceback.print_exc()
			raise Http404(traceback)

	else:
		raise Http404
