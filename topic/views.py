#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import Http404
from .models import  Topiccommentreply,   Topicwritereply, Topicusercomment, Group, Topic, TopicForm, CollectionTopic, Groupmanager, TopicLike
from django.contrib import messages
from article.form import CommentForm
from comment.models import Comment
from accounts.models import MyUser
import json
from django.http import HttpResponse
import traceback 
from notifications.signals import notify
from notifications.models import Notification
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from notifications.atwho import atwho
from django.views.decorators.cache import cache_page
from itertools import chain
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import datetime
from datetime import timedelta
from django.conf import settings
from article.tasks import topiccommentreplyplus,  topicwritereplyplus, topiccommentplus, readersin, add, instancesave, topiczanplus, topiczanminus, instancedelete
from django.core.cache import cache
from django.core.urlresolvers import reverse
# from .forms import TopicForm
GROUP_ALL_GROUP_TIMERANGE = 30#话题组首页显示的话题的时间范围
TOPIC_DETAIL_HOTCOMMENT_READERSRANGE = 3 #最热回复的门限制
TOPIC_DETAIL_HOTTOPIC_TIMERAGE = 99#话题页右侧热门话题的时间范围
import os
# Create your views here.
#话题组首页
def group_all(request):
	group = Group.objects.all().order_by("-topicount")
	#最近一个按热度排序; timestamp__gte=datetime.date.today(): 时间大于今天
	topic = Topic.objects.all().filter(timestamp__gte=datetime.date.today() - timedelta(days=GROUP_ALL_GROUP_TIMERANGE)).order_by("-readers")[0:10]
	context = {
		'group': group,
		'topic': topic,
		}
	return render(request, 'group_all.html',  context)

#更多话题按钮
def moretopic(request):
	if request.is_ajax():
		request.session['grouplen'] = request.POST.get('grouplen')
		grouplen = int(request.session['grouplen'])
		topic = Topic.objects.all().filter(timestamp__gte=datetime.date.today() - timedelta(days=GROUP_ALL_GROUP_TIMERANGE)).order_by("-readers")
	if topic.count() == grouplen:
		loadcompleted = '已全部加载完成'
	else:
		loadcompleted = '点击加载更多'
	data = {
		"loadcompleted": loadcompleted,
	}	
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')

#加载更多话题页
def groupage(request):
	if request.session.get('grouplen', False):
		grouplen = request.session['grouplen']
	topic = Topic.objects.all().filter(timestamp__gte=datetime.date.today() - timedelta(days=GROUP_ALL_GROUP_TIMERANGE))
	grouplen = int(grouplen)
	topic = topic[grouplen:grouplen+5]
	context = {
		"topic": topic,
	}
	return render(request, 'groupage.html',  context)

#不用
def group_index(request):
	topic = Topic.objects.order_by('-updated')

	context = {
		'topic': topic,
		}
	return render(request, 'group_index.html',  context)

#话题组首页
def group_detail(request, group_id):
	try:
		group = Group.objects.get(pk=group_id)
#		groupall = Group.objects.all().order_by("-topicount")
		topic = group.topic_set.all().order_by("-updated").filter(savetext = False).exclude(pk=142).exclude(pk=171)
		managers = Groupmanager.objects.filter(group = group)
		topicstickied1 = Topic.objects.get(pk=142)
		topicstickied2 = Topic.objects.get(pk=171)
		topicstickied = [topicstickied1, topicstickied2]
		# 分页
		paginator = Paginator(topic, 16)
		page = request.GET.get('page')
		if page and int(page)>1:
			topicstickied = None
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
		request.session['group'] = group.title
		request.session['lastpage'] = request.get_full_path()
		hottopic = Topic.objects.filter(group=group).filter(timestamp__gte=datetime.date.today() - timedelta(days=TOPIC_DETAIL_HOTTOPIC_TIMERAGE)).exclude(pk=142).exclude(pk=171).order_by('-readers')[0:5]
		scorerank=MyUser.objects.exclude(pk=53).exclude(pk=519).order_by('-score')[0:5]
		context = {
			'hottopic': hottopic,
			'group': group,
			'topic': contacts,
			'managers': managers,
			'topicstickied': topicstickied,
			'scorerank':scorerank,
			}
	except Group.DoesNotExist:
		raise Http404("Does not exist")
	return render(request, 'group_detail.html',  context)


# @cache_page(60 * 15)
#话题首页
def topic_detail(request, topic_id):
	try:
		topic = Topic.objects.get(pk=topic_id)
		user = topic.writer
		sender = request.user
		if user == sender:
			host = True
		else:
			host = False
	except Topic.DoesNotExist:
		raise Http404("Does not exist")
	#count = Comment.objects.filter(topic=topic).count()
	# 按时间顺序排序
	comment = Comment.objects.filter(topic=topic).filter(parent=None).order_by('timestamp')
	# 前三个回复是最热回复;  readers__gt=3 = readers 大于3
	commentorderbyreaders = Comment.objects.filter(topic=topic).filter(parent=None).filter(readers__gt=TOPIC_DETAIL_HOTCOMMENT_READERSRANGE).order_by('-readers')[0:3]
	#最新话题
	#newtopic = Topic.objects.filter(group=topic.group).order_by('-timestamp')[0:3]
	#最热话题
	hottopic = Topic.objects.filter(group=topic.group).filter(timestamp__gte=datetime.date.today() - timedelta(days=TOPIC_DETAIL_HOTTOPIC_TIMERAGE)).order_by('-readers')[0:5]
	#当前读者对象
	user = request.user
	#读者是否收藏该文章
	collection = CollectionTopic.objects.filter(topic=topic, user=user.id)
	print type(collection)
	if collection: 
		collection = '已收藏'
	else:
		collection = '收藏'
	# 分页
	paginator = Paginator(comment, 12)
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
	# If page is not an integer, deliver first page.
		contacts = paginator.page(1)
	except EmptyPage:
	# If page is out of range (e.g. 9999), deliver last page of results.
		contacts = paginator.page(paginator.num_pages)
	# topic.readers += 1
	# topic.save()
	readersin.delay(topic)
	#缓存的readers 增加1
	cachekey = "topic_readers_" + str(topic_id)
	if cache.get(cachekey) != None:
		cache.incr(cachekey)
	else:
		cache.set(cachekey, topic.readers, settings.CACHE_EXPIRETIME)

	#如果页数大于1则不显示最热回复
	ifhotcomment = True;
	if page:
		page = int(page)
		if page > 1:
			ifhotcomment = None;
	else:
		page = 1;
	request.session['lastpage'] = request.get_full_path()
	sharelink = request.get_host()+request.get_full_path()

	try:
		topiclike = TopicLike.objects.get(topic=topic, user=user)
		topiclike = True
	except:
		topiclike = False
	context = {
		'topic':topic,
		'user':user,
		"form": CommentForm,
		"submit_btn": "发表",
		"comment": comment,
		'contacts': contacts,
		#"count": count,
		#"newtopic": newtopic,
		"group": topic.group,
		"hottopic": hottopic,
		"commentorderbyreaders":commentorderbyreaders,#热门回复
		"ifhotcomment": ifhotcomment,
		'page': page,
		'sharelink': sharelink,
		'collection': collection,
		'host': host,
		'topiclike': topiclike,
	}
	#print "topic_detail"
	return render(request, 'topic_detail.html',  context)

#生成新的话题页
@login_required(login_url='/user/loggin/')
def newtopic(request):
	grouptitle = request.session.get('group', False)
	group = Group.objects.get(title = grouptitle)
	# group = False
	if request.method == 'POST':
		content = request.POST.get('content')
		title = request.POST.get('title')
		new_topic = Topic()
		new_topic.content = content
		if request.POST.get('savetext') == "True":
			new_topic.savetext = True
		else:
			new_topic.savetext = False
		new_topic.title = title
		new_topic.writer = request.user
		new_topic.group = group
		new_topic.save()
		group.topicount += 1
		instancesave.delay(group)
		cachekey = "topic_user_count_" + str(request.user.id)
		if cache.get(cachekey) != None:
			cache.incr(cachekey)
		else:
			usertopicnum = Topic.objects.filter(writer = request.user).count()
			cache.set(cachekey,  usertopicnum)
		cachekey = "group_topic_count_" + str(group.id)
		if cache.get(cachekey) != None:
			cache.incr(cachekey)
		else:
			group = Group.objects.get(id=group.id)
			cache.set(cachekey,  group.topicount)
		userlist = atwho(text = content, sender = request.user, targetcomment = None, targetproducts = None
						, targetarticle = None, targetopic = new_topic)
		return redirect(reverse("topic_detail", kwargs={"topic_id": new_topic.id}))
	else:
		print  request.user
		context = {
			'myform': TopicForm,
			'group': group,
			}
	return render(request, 'newtopic.html',  context)


def dianzan(request):
	topicid = request.POST.get('topicid')
	user = request.user
	try:
		topic = Topic.objects.get(id = topicid)
	except Article.DoesNotExist:
		raise Http404("Article does not exist")
	try:
		topiclike = TopicLike.objects.get(topic=topic, user=user)
	except:
		topiclike = None
	if topiclike: 
		topiclikecount = -1
		#topiclike.delete()
		instancedelete.delay(topiclike)
		#减去缓存中评论点赞数
		cachekey = "topic_like_count_" + str(topicid)
		if cache.get(cachekey) != None:
			cache.decr(cachekey)
		else:
			cache.set(cachekey,  topic.topiclike_set.count())
			cache.decr(cachekey)
		# if thidauth2(user, topic.writer, topic):
		# 	user.score = user.score - 5
		# 	instancesave.delay(user)
		# else:
		# 	pass
		topiczanminus.delay(user, topic.writer, topic)
	else:
		topiclikecount = +1
		#加上缓存中评论点赞数
		cachekey = "topic_like_count_" + str(topicid)
		if cache.get(cachekey) != None:
			cache.incr(cachekey)
		else:
			cache.set(cachekey,  topic.topiclike_set.count())
			cache.incr(cachekey)
		c = TopicLike(user=user, topic=topic)
		instancesave.delay(c)
		# if thidauth2(user, topic.writer, topic):
		# 	user.score = user.score + 5
		# 	instancesave.delay(user)
		# else:
		# 	pass
		topiczanplus.delay(user, topic.writer, topic)
	data = {
	 'topiclikecount': topiclikecount,
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')



#编辑话题
@login_required(login_url='/user/loggin/')
def renewtopic(request, topic_id):
	try:
		topic = Topic.objects.get(pk=topic_id)
		user = topic.writer
		sender = request.user
		if user == sender:
			pass
		else:
			return redirect(request.session['lastpage'])
	except Topic.DoesNotExist:
		raise Http404("Does not exist")
	if request.method == 'POST':
		content = request.POST.get('content')
		title = request.POST.get('title')
		topic.content = content
		topic.title = title
		if request.POST.get('savetext') == "True":
			topic.savetext = True
		else:
			topic.savetext = False
		topic.save()
		return redirect(reverse("topic_detail", kwargs={"topic_id": topic.id}))
	else:
		myform = TopicForm(instance=topic)
		context = {
			'myform': myform,
			'topic': topic,
			}
	return render(request, 'renewtopic.html',  context)


#ajax，发送评论,post
def topicomment(request):
	if request.is_ajax() and request.method == 'POST':
#		print request.POST.get('comment')
		text = request.POST.get('comment')
		topicid = request.POST.get('topicid')
		topic = Topic.objects.get(pk=topicid)
#		print request.POST.get('comment')
#		print request.POST.get('topicid')
		user = request.user
#		print user
		try:
			c = Comment(user=user, topic=topic, text=text)
			c.save()
			userlist = atwho(text = text, sender = user, targetcomment = c, targetproducts = None
							, targetarticle = None, targetopic = topic)#优先发送@消息
			for item in userlist:
				atwhouser = MyUser.objects.get(username = item)
				test = "@<a href='" +'/user/'+str(atwhouser.id)+'/informations/'+"'>"+atwhouser.username+"</a>"+' '
				test1 = "@<a href='" +'/user/'+str(atwhouser.id)+'/informations/'+"'>"+atwhouser.username+"</a>"+'&nbsp;'
				text = text.replace('@'+item+' ', test);
				text = text.replace('@'+item+'&nbsp;', test1);
			if topic.writer != user and topic.writer.username not in userlist:#再发送回复话题消息
				notify.send(sender=user, target_object= c
						, recipient = topic.writer, verb='#'
						, text=text, target_article = None
						, target_products = None
						, target_topic = topic)
				cachekey = "user_unread_count" + str(topic.writer.id)
				if cache.get(cachekey) != None:
					cache.incr(cachekey)
				else:
					unread = Notification.objects.filter(recipient = topic.writer).filter(read = False).count()
					cache.set(cachekey,  unread, settings.CACHE_EXPIRETIME)

                        topic.updated = timezone.now()
                        instancesave.delay(topic)
                        cachekey = "topic_comment_" + str(topicid)
                        if cache.get(cachekey) != None:
                                cache.incr(cachekey)
                        else:
                                cache.set(cachekey, topic.comment_set.count(), settings.CACHE_EXPIRETIME)

			cachekey = "comment_user_count_" + str(user.id)
			if cache.get(cachekey) != None:
				cache.incr(cachekey)
			else:
				usercomnum = Comment.objects.filter(user = user).count()
				cache.set(cachekey,  usercomnum)
			cachekey = "topic_comment_noparent_" + str(topicid)
			if cache.get(cachekey) != None:
				cache.incr(cachekey)
			else:
				cache.set(cachekey, Comment.objects.filter(topic=topic).filter(parent = None).count(), settings.CACHE_EXPIRETIME)
			try:
				topicusercomment = Topicusercomment.objects.get(topic=topic, user=user)
			except:
				topicusercomment = None
			if topicusercomment or topic.writer == user:
				pass
			else:
				topiccommentplus.delay(topic.writer, user, topic, Topicusercomment)
			
			data = {
			"user": user.username,
			"text": text,
			"commentid": c.id
			}
#			print data['commentid']
			json_data = json.dumps(data)
			print 'data'
			return HttpResponse(json_data, content_type='application/json')
		except:
			traceback.print_exc()
			raise Http404(traceback)
	else:
		raise Http404

#ajax，发送评论的评论,post
def topcommentcomment(request):
	if request.is_ajax() and request.method == 'POST':
		text = request.POST.get('comment')
		topicid = request.POST.get('topicid')
		#parenttext = request.POST.get('parenttext')
		preentid = request.POST.get('preentid')
		topic = Topic.objects.get(pk=topicid)
		comment = Comment.objects.filter(topic=topic)
		targetcomment = Comment.objects.get(pk=preentid)
		user = request.user
		try:
			c = Comment(user=user, topic=topic, text=text, parent=targetcomment)
			c.save()
			userlist = atwho(text = text, sender = user, targetcomment = c, targetproducts = None
							, targetarticle = None, targetopic = topic)#优先发送@消息
			for item in userlist:
				atwhouser = MyUser.objects.get(username = item)
				test = "@<a href='" +'/user/'+str(atwhouser.id)+'/informations/'+"'>"+atwhouser.username+"</a>"+' '
				text = text.replace('@'+item+' ', test);


			if targetcomment.user != user and targetcomment.user.username not in userlist:#再发送回复评论消息
				notify.send(sender=user, target_object= c
						, recipient = targetcomment.user, verb='$'
						, text=text, target_article = None
						, target_products = None
						, target_topic = topic)
				cachekey = "user_unread_count" + str(targetcomment.user.id)
				if cache.get(cachekey) != None:
					cache.incr(cachekey)
				else:
					unread = Notification.objects.filter(recipient = targetcomment.user.id).filter(read = False).count()
					cache.set(cachekey,  unread, settings.CACHE_EXPIRETIME)

			if topic.writer != user and topic.writer.username not in userlist and not (targetcomment.user != user and targetcomment.user.username not in userlist):#再发送回复话题消息
				notify.send(sender=user, target_object= c
						, recipient = topic.writer, verb='#'
						, text=text, target_article = None
						, target_products = None
						, target_topic = topic)
				cachekey = "user_unread_count" + str(topic.writer.id)
				if cache.get(cachekey) != None:
					cache.incr(cachekey)
				else:
					unread = Notification.objects.filter(recipient = topic.writer).filter(read = False).count()
					cache.set(cachekey,  unread, settings.CACHE_EXPIRETIME)
			topic.updated = timezone.now()
			instancesave.delay(topic)
			cachekey = "comment_user_count_" + str(user.id)
			if cache.get(cachekey) != None:
				cache.incr(cachekey)
			else:
				usercomnum = Comment.objects.filter(user = user).count()
				cache.set(cachekey,  usercomnum)
			cachekey = "topic_comment_" + str(topicid)
			if cache.get(cachekey) != None:
				cache.incr(cachekey)
			else:
				cache.set(cachekey, topic.comment_set.count(), settings.CACHE_EXPIRETIME)
			readersin(targetcomment)
			# c = Comment(user=user, topic=topic, text=text, parent=targetcomment)
			# c.save()

			try:
				topicusercomment = Topicusercomment.objects.get(topic=topic, user=user)
			except:
				topicusercomment = None
			if topicusercomment or topic.writer == user:
				pass
			else:
				topiccommentplus.delay(topic.writer, user, topic, Topicusercomment)


			try:
				topicwritereply = Topicwritereply.objects.get(topic=topic, user=targetcomment.user)
			except:
				topicwritereply = None
			if topicwritereply == None and user == topic.writer and targetcomment.user != user:
				topicwritereplyplus.delay(topic.writer, targetcomment.user, topic, Topicwritereply)
			else:
				pass


			try:
				topiccommentreply1 = Topiccommentreply.objects.get(topic=topic, user1=user, user2 = targetcomment.user)
			except:
				topiccommentreply1 = None
			try:
				topiccommentreply2 = Topiccommentreply.objects.get(topic=topic, user1=targetcomment.user, user2 = user)
			except:
				topiccommentreply2 = None
			if topiccommentreply1 == None and topiccommentreply2 == None and user != topic.writer and targetcomment.user != user:
				topiccommentreplyplus.delay(topic.writer, targetcomment.user, user, topic, Topiccommentreply)
			else:
				pass



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

#收藏话题
def collectiontopic(request):
	print 'collection'
	try:
		topicid = request.POST.get('topicid')
		topic = Topic.objects.get(pk=topicid)
		user = request.user
	except Topic.DoesNotExist:
		raise Http404("Topic does not exist")
	collection = CollectionTopic.objects.filter(topic=topic, user=user)
	print type(collection)
	if collection: 
		collection.delete()
		collecicon = '收藏'
	else:
		c = CollectionTopic(user=user, topic=topic)
		c.save()
		collecicon = '已收藏'
	data = {
	 'collecicon': collecicon,
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


#ajax，fortest
# def atwhoidentify(request):
# 	if request.is_ajax():
# 		text = request.POST.get('comment')
# 		print text
# 		userlist = atwhononoti(text)
# 		print 'userlist'
# 		print userlist
# 		data = {
# 			"userlist": userlist,
# 			}
# 		json_data = json.dumps(data)
# 		return HttpResponse(json_data, content_type='application/json')
# 	else:
# 		raise Http404

@login_required(login_url='/user/loggin/')
def mobilenew(request):
	grouptitle = request.session.get('group', False)
	group = Group.objects.get(title = grouptitle)
	if request.method == 'POST':
		content = request.POST.get('content')
		title = request.POST.get('title')
		image = request.FILES.getlist('img')
		new_topic = Topic()
		new_topic.content = content
		new_topic.title = title
		new_topic.writer = request.user
		new_topic.group = group
		# new_topic.save()
		group.topicount += 1
		instancesave.delay(group)
		try:
			new_topic.images1 = image[0]
			imgadd = '<p><img alt="" src="/static/media/images/'+str(image[0])+'" style=" width:100%" /></p>'
			new_topic.content = new_topic.content + imgadd			
		except: 
			pass
		try:
			new_topic.images2 = image[1]
			imgadd = '<p><img alt="" src="/static/media/images/'+str(image[1])+'" style=" width:100%" /></p>'
			new_topic.content = new_topic.content + imgadd	
		except: 
			pass
		try:
			new_topic.images3 = image[2]
			imgadd = '<p><img alt="" src="/static/media/images/'+str(image[2])+'" style=" width:100%" /></p>'
			new_topic.content = new_topic.content + imgadd		
		except: 
			pass
		try:	
			new_topic.images4 = image[3]
			imgadd = '<p><img alt="" src="/static/media/images/'+str(image[3])+'" style=" width:100%" /></p>'
			new_topic.content = new_topic.content + imgadd	
		except: 
			pass
		try:	
			new_topic.images5 = image[4]
			imgadd = '<p><img alt="" src="/static/media/images/'+str(image[4])+'" style=" width:100%" /></p>'
			new_topic.content = new_topic.content + imgadd	
		except: 
			pass
		try:
			new_topic.images6 = image[5]
			imgadd = '<p><img alt="" src="/static/media/images/'+str(image[5])+'" style=" width:100%" /></p>'
			new_topic.content = new_topic.content + imgadd		
		except: 
			pass

		if request.POST.get('savetext') == "True":
			new_topic.savetext = True
		else:
			new_topic.savetext = False

		new_topic.save() 

		cachekey = "topic_user_count_" + str(request.user.id)
		if cache.get(cachekey) != None:
			cache.incr(cachekey)
		else:
			usertopicnum = Topic.objects.filter(writer = request.user).count()
			cache.set(cachekey,  usertopicnum)
		cachekey = "group_topic_count_" + str(group.id)
		if cache.get(cachekey) != None:
			cache.incr(cachekey)
		else:
			group = Group.objects.get(id=group.id)
			cache.set(cachekey,  group.topicount)
		userlist = atwho(text = new_topic.content, sender = request.user, targetcomment = None, targetproducts = None
						, targetarticle = None, targetopic = new_topic)
		return redirect(reverse("topic_detail", kwargs={"topic_id": new_topic.id}))
	context = {
		'group': group,
		}
	return render(request, 'mobilenew.html',  context)
