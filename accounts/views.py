#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from .form import LoginForm, RegisterForm
from .models import MyUser, MyUserIconForm

from notifications.models import Notification
# from comment.models import Comment
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
from django.http import HttpResponse
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404 
from notifications.signals import notify
from topic.models import CollectionTopic, Topic
from article.models import Collection, Article
from company.models import Company, CollectionCompany
from comment.models import Comment
from notifications.models import Notification
from article.tasks import readersin, add, readersout, instancedelete, instancesave
import os
from django.core.cache import cache
from django.conf import settings
from investment.models import Investment, CollectionInvestment
#登录页面
def loggin(request):
	form = LoginForm(request.GET or None)
	next_url = request.GET.get('next')
	action_url = reverse("loggin")
	if form.is_valid():
		human = True
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			if request.POST.get('checkbox'):
				request.session.set_expiry(1209600*2)
			if request.session.get('lastpage', False):
				return redirect(request.session['lastpage'])
			else:
				return redirect('home')
		else:
			messages.error(request, '用户名与密码不匹配，请重新输入！')
	context = {
		"form": form,
		"action_url": action_url,
		"submit_btn": "登录",
		}
	return render(request, 'loggin.html',  context)


#登出，不用
def userlogout(request):
	logout(request)
	if request.session.get('lastpage', False):
		return redirect(request.session['lastpage'])
	else:
		return redirect('home')


#注册页面
def register(request):
	form = RegisterForm(request.POST or None)
	action_url = reverse("register")
	if form.is_valid():
		human = True
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password2')
		new_user = MyUser()
		new_user.username = username
		new_user.email = email
		new_user.set_password(password) #RIGHT
		new_user.save()
		#注册成功后直接登录
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
		else:
			return redirect(reverse('register'))
		#return render(request,'base_1.html')
		return redirect(reverse('home'))
	context = {
		"form": form,
		"action_url": action_url,
		"submit_btn": "注册",
		}
	return render(request, 'register.html',  context)


#ajax，在注册和登录页面验证码刷新
def captchaview(request):
	if request.is_ajax():
		captchakey = CaptchaStore.generate_key()
		acptchaimg = captcha_image_url(captchakey)
		data = {
			"captchakey": captchakey,
			"acptchaimg": acptchaimg,
		}
		json_data = json.dumps(data)
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404


#ajax，在注册页面验证用户名是否已被注册
def accountsview(request):
	if request.is_ajax() and request.method == 'POST':
		username = request.POST.get('username')
        try:
			exists = MyUser.objects.get(username=username)
			data = {
				"message": '该用户名已被注册',
				'classname': 'errorlist',
			}
			json_data = json.dumps(data)
			return HttpResponse(json_data, content_type='application/json')
        except MyUser.DoesNotExist:
			data = {
				"message": '恭喜，该用户名可注册！',
				'classname': 'successlist',
				'register': 'Ture'
			}
			json_data = json.dumps(data)
			return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404

#我的主页
def userdashboardinformations(request, user_id):	
	try:
		user = MyUser.objects.get(pk=user_id)
		sender = request.user
		if user == sender:
			host = True
			hostname = '我的'
		else:
			host = False
			hostname = '他的'
		action_url = reverse("user_detailinformations", kwargs={"user_id": user_id})
		if request.method == 'POST' and request.FILES.get('img', False):
			image = request.FILES['img']
			user.icon = image
			user.save() 
			os.system('echo yes | python /home/shen/Documents/paperproject/mynewspaper/manage.py collectstatic')
			return redirect(action_url)
		if request.method == 'POST' and request.POST.get('emailaddress', False):
			emailaddress = request.POST.get('emailaddress')
			user.email = emailaddress
			user.save()
			return redirect(action_url)
		if request.method == 'POST' and request.POST.get('password', False):
			print request.POST.get('password')
			password = request.POST.get('password')
			user.set_password(password)
			user.save()
			return redirect(action_url)
		if request.method == 'POST' and request.POST.get('privcycomment', False):
			text = request.POST.get('privcycomment')
			try:
				# c = Comment(user=user, is_privcycomment=True, text=text)
				notify.send(sender=sender, target_object=None, recipient = user, verb="_@_", text=text)
			except:
				traceback.print_exc()
			return redirect(action_url)
		else:
			context = {
			"userofinfor": user,
			'host': host,
			'hostname': hostname,
			#"action_url": action_url,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_detailinformations.html',  context)

#我的评论
def userdashboardcomments(request, user_id):	
	try:
		user = MyUser.objects.get(pk=user_id)
		sender = request.user
		if user == sender:
			host = True
			hostname = '我的'
		else:
			host = False
			hostname = '他的'
		user = MyUser.objects.get(pk=user_id)
		comment = user.comment_set.all().filter(parent = None) 
		# 分页
		paginator = Paginator(comment, 10)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)

		context = {
			'userofinfor': user,
			"comment": contacts,
			'hostname': hostname,
			'host': host,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_detailcomments.html',  context)

#我的消息，@我
def userdashboardnotifications(request, user_id):	
	try:
		user = MyUser.objects.get(pk=user_id)
		sender = request.user
		if user == sender:
			host = True
			hostname = '我的'
		else:
			host = False
			hostname = '他的'
		notifications = Notification.objects.filter(recipient = user).filter(verb = '@').order_by("-timestamp")
		# 分页
		paginator = Paginator(notifications, 10)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
		context = {
			'userofinfor': user,
			"notifications": contacts,
			'host': host,
			'hostname': hostname,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_detailnotifications.html',  context)

#我的消息-私信
def privcynotifications(request, user_id):
	try:
		user = MyUser.objects.get(pk=user_id)
		sender = request.user
		if user == sender:
			host = True
			hostname = '我的'
		else:
			host = False
			hostname = '他的'
		notifications = Notification.objects.filter(recipient = user).filter(verb = '_@_').order_by("-timestamp")
		# 分页
		paginator = Paginator(notifications, 10)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
		context = {
			'userofinfor': user,
			"notifications": contacts,
			'host': host,
			'hostname': hostname,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_privcynotifications.html',  context)

#我的收藏
def userdashboardcollections(request, user_id):	
	try:
		user = MyUser.objects.get(pk=user_id)
		sender = request.user
		if user == sender:
			host = True
			hostname = '我的'
		else:
			host = False
			hostname = '他的'
		collection = Collection.objects.filter(user = user).order_by('-id')
		# 分页
		paginator = Paginator(collection, 10)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
		context = {
			'collection' : contacts,
			'host': host,
			'userofinfor': user,
			'hostname': hostname,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_detailcollections.html',  context)

#我的收藏-话题
def userdashboardcollectionstopic(request, user_id):	
	try:
		user = MyUser.objects.get(pk=user_id)
		sender = request.user
		if user == sender:
			host = True
			hostname = '我的'
		else:
			host = False
			hostname = '他的'
		collection = CollectionTopic.objects.filter(user = user).order_by('-id')
		# 分页
		paginator = Paginator(collection, 10)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
		context = {
			'collection' : contacts,
			'host': host,
			'userofinfor': user,
			'hostname': hostname,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_userdashboardcollectionstopic.html',  context)


#我的收藏-公司
def userdashboardcollectionscompany(request, user_id):	
	try:
		user = MyUser.objects.get(pk=user_id)
		sender = request.user
		if user == sender:
			host = True
			hostname = '我的'
		else:
			host = False
			hostname = '他的'
		collection = CollectionCompany.objects.filter(user = user).order_by('-id')
		# 分页
		paginator = Paginator(collection, 10)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
		context = {
			'collection' : contacts,
			'host': host,
			'userofinfor': user,
			'hostname': hostname,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_userdashboardcollectionscompany.html',  context)

#我的收藏-机构
def userdashboardcollectionsinvestment(request, user_id):	
	try:
		user = MyUser.objects.get(pk=user_id)
		sender = request.user
		if user == sender:
			host = True
			hostname = '我的'
		else:
			host = False
			hostname = '他的'
		collection = CollectionInvestment.objects.filter(user = user).order_by('-id')
		# 分页
		paginator = Paginator(collection, 10)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
		context = {
			'collection' : contacts,
			'host': host,
			'userofinfor': user,
			'hostname': hostname,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_userdashboardcollectionsinvestment.html',  context)


#我的评论-点评
def userdashboard_commentocomment(request, user_id):	
	try:
		user = MyUser.objects.get(pk=user_id)
		if user == request.user:
			host = True
			hostname = '我的'
		else:
			host = False
			hostname = '他的'
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	comment = user.comment_set.all().exclude(parent = None) 
	# 分页
	paginator = Paginator(comment, 10)
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
	# If page is not an integer, deliver first page.
		contacts = paginator.page(1)
	except EmptyPage:
	# If page is out of range (e.g. 9999), deliver last page of results.
		contacts = paginator.page(paginator.num_pages)
	context = {
		"comment": contacts,
		'hostname': hostname,
		'userofinfor': user,
		'host': host,
	}
	return render(request, 'userdashboard_commentocomment.html',  context)

#我的文章
def userdashboardarticle(request, user_id):
	try:
		user = MyUser.objects.get(pk=user_id)
		sender = request.user
		if user == sender:
			host = True
			hostname = '我的'
		else:
			host = False
			hostname = '他的'
		article = Article.objects.filter(writer = user).order_by("-timestamp")
		print article.count()
		# 分页
		paginator = Paginator(article, 10)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
		context = {
			'article' : contacts,
			'host': host,
			'userofinfor': user,
			'hostname': hostname,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_userdashboardarticle.html',  context)

#我的公司
def userdashboardcompany(request, user_id):
	try:
		user = MyUser.objects.get(pk=user_id)
		sender = request.user
		if user == sender:
			host = True
			hostname = '我的'
		else:
			host = False
			hostname = '他的'
		company = Company.objects.filter(uper = user).filter(verify = True).order_by("-id")
		# 分页
		paginator = Paginator(company, 10)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
		context = {
			'company' : contacts,
			'host': host,
			'userofinfor': user,
			'hostname': hostname,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_userdashboardcompany.html',  context)

#我的话题
def userdashboardarticletopic(request, user_id):
	try:
		user = MyUser.objects.get(pk=user_id)
		sender = request.user
		if user == sender:
			host = True
			hostname = '我的'
		else:
			host = False
			hostname = '他的'
		topic = Topic.objects.filter(writer = user).order_by("-timestamp")
		# 分页
		paginator = Paginator(topic, 10)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
		context = {
			'topic' : contacts,
			'host': host,
			'userofinfor': user,
			'hostname': hostname,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_userdashboardarticletopic.html',  context)


#ajax删除我的的评论，我的收藏....
def deleteinfo(request):
	try:
		instancetable = {
			'Comment':Comment,
			'Notification':Notification,
			'Collection': Collection,
			'CollectionTopic': CollectionTopic,
			'Topic': Topic,
			'CollectionCompany': CollectionCompany,
			'CollectionInvestment': CollectionInvestment,
		}
		instanceid = request.POST.get('instanceid')
		instancetype = request.POST.get('instancetype')
		instace = instancetable.get(instancetype).objects.get(pk=instanceid)
		#instace.delete()
		instancedelete.delay(instace)
		data = {
			"test": 'test',
		}
		json_data = json.dumps(data)
	except:
		traceback.print_exc()
	return HttpResponse(json_data, content_type='application/json')


def inbox(request):
	if request.is_ajax():
		cachekey = "user_unread_count" + str(request.user.id)
		if cache.get(cachekey) != None:
			unread = cache.get(cachekey)
		else:
			unread = Notification.objects.filter(recipient = request.user).filter(read = False).count()
			cache.set(cachekey,  unread, settings.CACHE_EXPIRETIME)
		data = {
			"unread": unread,
		}
		json_data = json.dumps(data)
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404


#测试用函数
def test(request):	
	test = Article.objects.all()
	print test.count()
	context = {
		'test':test,
		}
	return render(request, 'test.html', context)
