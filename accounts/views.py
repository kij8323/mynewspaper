#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from .form import LoginForm, RegisterForm, RepasswordForm

from .models import MyUser, MyUserIconForm, Repassworduser, WeiboUser, WeixinUser

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
import datetime 

from django.contrib.auth.decorators import login_required

from products.models import Products, Application

from weibo import APIClient

import traceback 
#登录页面
def loggin(request):
	if request.GET.get('username'):
		form = LoginForm(request.GET)
	else:
		form = LoginForm(None)
	weixinurl = "https://open.weixin.qq.com/connect/qrconnect?appid=wx59a3f67caac61d02&redirect_uri=http://www.wutongnews.com/user/loggin/weixin&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect"

	weixinurlgongzhong = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx59a3f67caac61d02&redirect_uri=http://www.wutongnews.com/user/loggin/weixin&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect"


	APP_KEY = '2155349390' # app key
	APP_SECRET = 'bf5f82094e791b582ffb3489dcfa8a96' # app secret
	CALLBACK_URL = 'http://www.wutongnews.com/user/loggin/third'
	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
	url = client.get_authorize_url()
	next_url = request.GET.get('next')
	action_url = reverse("loggin")
	if form.is_valid():
		human = True
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			try:
				weibouser = WeiboUser.objects.get(user = user)
				weibouser.logpassword = password
				weibouser.save()
			except:
				pass
			try:
				weixinuser = WeixinUser.objects.get(user = user)
				weixinuser.logpassword = password
				weixinuser.save()
			except:
				pass
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
		"url": url,
		"weixinurl": weixinurl,
		"weixinurlgongzhong": weixinurlgongzhong,
		}
	return render(request, 'loggin.html',  context)


def thirdfirstloggin(request, user_id):
	myuser = MyUser.objects.get(id = user_id)
	if request.GET.get('username'):
		form = LoginForm(request.GET)
	else:
		form = LoginForm(None)
	if form.is_valid():
		human = True
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			try:
				weibouser = WeiboUser.objects.get(user = user)
				weibouser.logpassword = password
				weibouser.save()
			except:
				pass
			try:
				weixinuser = WeixinUser.objects.get(user = user)
				weixinuser.logpassword = password
				weixinuser.save()
			except:
				pass
			if request.POST.get('checkbox'):
				request.session.set_expiry(1209600*2)
			if request.session.get('lastpage', False):
				return redirect(request.session['lastpage'])
			else:
				return redirect('home')
		else:
			messages.error(request, '用户名与密码不匹配，请重新输入！')
	context = {
	"myuser": myuser,
	"form": form,
	}
	return render(request, 'repassweixin.html',  context)


#登录页面
def logginweibo(request):
	if request.GET.get('username'):
		form = LoginForm(request.GET)
	else:
		form = LoginForm(None)
	weixinurl = "https://open.weixin.qq.com/connect/qrconnect?appid=wx59a3f67caac61d02&redirect_uri=http://www.wutongnews.com/user/loggin/weixin&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect"
	weixinurlgongzhong = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx59a3f67caac61d02&redirect_uri=http://www.wutongnews.com/user/loggin/weixin&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect"

	APP_KEY = '2155349390' # app key
	APP_SECRET = 'bf5f82094e791b582ffb3489dcfa8a96' # app secret
	CALLBACK_URL = 'http://www.wutongnews.com/user/loggin/third'
	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
	url = client.get_authorize_url()

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
		"url": url,
		"weixinurl": weixinurl,
		"weixinurlgongzhong": weixinurlgongzhong,
		}
	return render(request, 'logginweibo.html',  context)

#登录页面
def logginthird(request):
	if request.GET.get('username'):
		form = LoginForm(request.GET)
	else:
		form = LoginForm(None)

	APP_KEY = '2155349390' # app key
	APP_SECRET = 'bf5f82094e791b582ffb3489dcfa8a96' # app secret
	CALLBACK_URL = 'http://www.wutongnews.com/user/loggin/third'
	code = request.GET.get('code')
	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)


	try:
		r = client.request_access_token(code)
		access_token = r.access_token
		expires_in = r.expires_in
		client.set_access_token(access_token, expires_in)
		uid = client.account.get_uid.get()['uid']
		screen_name = client.users.show.get(uid=uid)['screen_name']
		weiboid = client.users.show.get(uid=uid)['id']
		profile_image_url = client.users.show.get(uid=uid)['profile_image_url']
		request.session['weiboid'] = weiboid
		request.session['screen_name'] = screen_name
		request.session['profile_image_url'] = profile_image_url
	except:
		if request.session.get('weiboid', False):
			weiboid = request.session['weiboid']
		if request.session.get('screen_name', False):
			screen_name = request.session['screen_name']
		if request.session.get('profile_image_url', False):
			profile_image_url = request.session['profile_image_url']
	next_url = request.GET.get('next')
	o_screen_name = screen_name
	o_profile_image_url = profile_image_url
	o_id = weiboid
	action_url = reverse("logginthird")
	try:
		loguser = WeiboUser.objects.get(weiboid=o_id)
		loguser.user.thirdicon = o_profile_image_url
		loguser.user.save()
		user = authenticate(username=loguser.user.username, password=loguser.logpassword)
		if user is not None:
			login(request, user)
			if request.POST.get('checkbox'):
				request.session.set_expiry(1209600*2)
			if request.session.get('lastpage', False):
				return redirect(request.session['lastpage'])
			else:
				return redirect('home')
		else:
			return redirect(reverse("thirdfirstloggin", kwargs={"user_id": loguser.user.id}))

	except:
		if str(request.GET.get('log')) == "directly-login":
			new_user = MyUser()
			count=True
			while (count == True):
				try:
					falsename = MyUser.objects.get(username= o_screen_name)
					o_screen_name = o_screen_name+'weibo'
				except:
					count = False
			new_user.username = o_screen_name
			new_user.set_password("wutong")
			new_user.thirdicon = o_profile_image_url
			new_user.save()
			loguser = WeiboUser()
			loguser.user = new_user
			loguser.weiboid = o_id
			loguser.weiboname = o_screen_name
			loguser.iconaddress = o_profile_image_url
			loguser.logpassword = "wutong"
			loguser.save()
			user = authenticate(username=o_screen_name, password="wutong")
			if user:
				login(request, user)
				if request.session.get('lastpage', False):
					return redirect(request.session['lastpage'])
				else:
					return redirect(reverse('home'))
			else:
				return redirect(reverse('register'))
		if form.is_valid():
			human = True
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				loguser = WeiboUser()
				loguser.user = user
				loguser.weiboid = o_id
				loguser.weiboname = o_screen_name
				loguser.iconaddress = o_profile_image_url
				loguser.logpassword = password
				loguser.save()
				print "loguser.save()"
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
		"submit_btn": "关联已有账户",
		"o_screen_name": o_screen_name,
		"o_profile_image_url": o_profile_image_url,
		"o_id": o_id,
		"screen_name": screen_name,
		"weiboid": weiboid,
		"profile_image_url": profile_image_url,
		}
	return render(request, 'logginthird.html',  context)

import urllib
import urllib2
def logginweixin(request):
	if request.GET.get('username'):
		form = LoginForm(request.GET)
	else:
		form = LoginForm(None)
	try:
		CODE = request.GET.get('code')
		url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx59a3f67caac61d02&secret=25fdbdc3e5ae5327111c97bba099ba28&code="+CODE+"&grant_type=authorization_code"
		req = urllib2.Request(url)
		res_data = urllib2.urlopen(req)
		res = res_data.readline()
		test = json.loads(res)['refresh_token']
		refreshurl = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=wx59a3f67caac61d02&grant_type=refresh_token&refresh_token="+str(test)
		rereq = urllib2.Request(refreshurl)
		reres_data = urllib2.urlopen(rereq)
		reres = reres_data.readline()
		access_token = json.loads(reres)['access_token']
		openid = json.loads(reres)['openid']
		authurl = "https://api.weixin.qq.com/sns/auth?access_token="+str(access_token)+"&openid="+str(openid)
		authreq = urllib2.Request(authurl)
		authres_data = urllib2.urlopen(authreq)
		authres = authres_data.readline()
		errmsg = json.loads(authres)['errmsg']
		if str(errmsg) == "ok":
			pass;
		else:
			return redirect('loggin')
		infourl = "https://api.weixin.qq.com/sns/userinfo?access_token="+str(access_token)+"&openid="+str(openid)
		inforeq = urllib2.Request(infourl)
		infores_data = urllib2.urlopen(inforeq)
		infores = infores_data.readline()
		nickname = str(json.loads(infores)['nickname'])
		headimgurl = str(json.loads(infores)['headimgurl'])
		unionid = str(json.loads(infores)['unionid'])
		request.session['nickname'] = nickname
		request.session['headimgurl'] = headimgurl
		request.session['unionid'] = unionid
	except:
		if request.session.get('nickname', False):
			nickname = request.session['nickname']
		if request.session.get('headimgurl', False):
			headimgurl = request.session['headimgurl']
		if request.session.get('unionid', False):
			unionid = request.session['unionid']
	next_url = request.GET.get('next')
	o_screen_name = nickname
	o_profile_image_url = headimgurl
	o_id = unionid
	action_url = reverse("logginweixin")
	try:
		loguser = WeixinUser.objects.get(weixinid=o_id)
		loguser.user.thirdicon = o_profile_image_url
		loguser.user.save()
		user = authenticate(username=loguser.user.username, password=loguser.logpassword)
		if user is not None:
			login(request, user)
			if request.POST.get('checkbox'):
				request.session.set_expiry(1209600*2)
			if request.session.get('lastpage', False):
				return redirect(request.session['lastpage'])
			else:
				return redirect('home')
		else:
			return redirect(reverse("thirdfirstloggin", kwargs={"user_id": loguser.user.id}))

	except:
		if str(request.GET.get('log')) == "directly-login":
			new_user = MyUser()
			count=True
			while (count == True):
				try:
					falsename = MyUser.objects.get(username= o_screen_name)
					o_screen_name = o_screen_name+'weixin'
				except:
					count = False
			new_user.username = o_screen_name
			new_user.set_password("wutong")
			new_user.thirdicon = o_profile_image_url
			new_user.save()
			loguser = WeixinUser()
			loguser.user = new_user
			loguser.weixinid = o_id
			loguser.weixinname = o_screen_name
			loguser.iconaddress = o_profile_image_url
			loguser.logpassword = "wutong"
			loguser.save()
			user = authenticate(username=o_screen_name, password="wutong")
			if user:
				login(request, user)
				if request.session.get('lastpage', False):
					return redirect(request.session['lastpage'])
				else:
					return redirect(reverse('home'))
			else:
				return redirect(reverse('register'))
		if form.is_valid():
			human = True
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				loguser = WeixinUser()
				loguser.user = user
				loguser.weixinid = o_id
				loguser.weixinname = o_screen_name
				loguser.iconaddress = o_profile_image_url
				loguser.logpassword = password
				loguser.save()
				print "loguser.save()"
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
		"submit_btn": "关联已有账户",
		"o_screen_name": o_screen_name,
		"o_profile_image_url": o_profile_image_url,
		"o_id": o_id,
		}
	return render(request, 'logginweixin.html',  context)



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
		password = request.POST.get('password2')
		new_user = MyUser()
		new_user.username = username
		new_user.set_password(password) #RIGHT
		new_user.save()
		#注册成功后直接登录
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			if request.session.get('lastpage', False):
				return redirect(request.session['lastpage'])
			else:
				return redirect(reverse('home'))
		else:
			return redirect(reverse('register'))
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
		try:
			weixinuser = WeixinUser.objects.get(user=user)
			weixinusername = weixinuser.weixinname
			weixinset=True
		except:
			weixinusername = '--'
			weixinset=False
		try:
			weibouser = WeiboUser.objects.get(user=user)
			weibousername = weibouser.weiboname
			weiboset=True
		except:
			weibousername = '--'
			weiboset=False


		weixinurl = "https://open.weixin.qq.com/connect/qrconnect?appid=wx59a3f67caac61d02&redirect_uri=http://www.wutongnews.com/user/weixin/connection&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect"

		weixinurlgongzhong = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx59a3f67caac61d02&redirect_uri=http://www.wutongnews.com/user/weixin/connection&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect"


		APP_KEY = '2155349390' # app key
		APP_SECRET = 'bf5f82094e791b582ffb3489dcfa8a96' # app secret
		CALLBACK_URL = 'http://www.wutongnews.com/user/weibo/connection'
		client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
		weibourl = client.get_authorize_url()


		action_url = reverse("user_detailinformations", kwargs={"user_id": user_id})
		if host and request.method == 'POST' and request.FILES.get('img', False):
			image = request.FILES['img']
			user.icon = image
			user.thirdicon = None
			user.save() 
			os.system('echo yes | python /home/shen/Documents/paperproject/mynewspaper/manage.py collectstatic')
			return redirect(action_url)
		if host and request.method == 'POST' and request.POST.get('emailaddress', False):
			emailaddress = request.POST.get('emailaddress')
			user.email = emailaddress
			user.save()
			return redirect(action_url)
		if host and request.method == 'POST' and request.POST.get('id_qianming', False):
			qianming = request.POST.get('id_qianming')
			user.qianming = qianming
			user.save()
			return redirect(action_url)
		if host and request.method == 'POST' and request.POST.get('phonenumber', False):
			phonenumber = request.POST.get('phonenumber')
			user.phonenumber = phonenumber
			user.save()
			return redirect(action_url)
		if host and request.method == 'POST' and request.POST.get('password', False):

			password = request.POST.get('password')
			user.set_password(password)
			user.save()
			try:
				weibouser = WeiboUser.objects.get(user = user)
				weibouser.logpassword = password
				weibouser.save()
			except:
				pass
			try:
				weixinuser = WeixinUser.objects.get(user = user)
				weixinuser.logpassword = password
				weixinuser.save()
			except:
				pass
			return redirect(action_url)
		if request.method == 'POST' and request.POST.get('privcycomment', False):
			text = request.POST.get('privcycomment')
			try:
				notify.send(sender=sender, target_object=None, recipient = user, verb="_@_", text=text)
				cachekey = "user_unread_count" + str(user.id)
				if cache.get(cachekey) != None:
					cache.incr(cachekey)
				else:
					unread = Notification.objects.filter(recipient = user).filter(read = False).count()
					cache.set(cachekey,  unread, settings.CACHE_EXPIRETIME)	

				cachekey = "user_privcyunread_count" + str(user.id)
				if cache.get(cachekey) != None:
					cache.incr(cachekey)
				else:
					unread = Notification.objects.filter(recipient = user).filter(read = False).filter(verb = '_@_').count()
					cache.set(cachekey,  unread, settings.CACHE_EXPIRETIME)	


			except:
				traceback.print_exc()
			return redirect(action_url)
		else:
			context = {
			"userofinfor": user,
			'host': host,
			'hostname': hostname,
			'weixinset': weixinset,
			'weiboset': weiboset,
			'weibousername': weibousername,
			'weixinusername': weixinusername,
			'weixinurlgongzhong': weixinurlgongzhong,
			'weixinurl': weixinurl,
			"weibourl": weibourl,
			#"action_url": action_url,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_detailinformations.html',  context)

@login_required(login_url='/user/loggin/')
def weiboconnection(request):
	try:
		action_url = reverse("user_detailinformations", kwargs={"user_id": request.user.id})
		APP_KEY = '2155349390' # app key
		APP_SECRET = 'bf5f82094e791b582ffb3489dcfa8a96' # app secret
		CALLBACK_URL = 'http://www.wutongnews.com/user/weibo/connection'
		code = request.GET.get('code')
		client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
		r = client.request_access_token(code)
		access_token = r.access_token
		expires_in = r.expires_in
		client.set_access_token(access_token, expires_in)
		uid = client.account.get_uid.get()['uid']
		screen_name = client.users.show.get(uid=uid)['screen_name']
		weiboid = client.users.show.get(uid=uid)['id']
		profile_image_url = client.users.show.get(uid=uid)['profile_image_url']
		try:
			weibouser = WeiboUser.objects.get(weiboid = weiboid)
			isweibouser = True
		except:
			isweibouser = False
		if isweibouser:
			raise Http404("微博帐号已经关联别的帐号")
		else:
			pass
		loguser = WeiboUser()
		loguser.user = request.user
		loguser.weiboid = weiboid
		loguser.weiboname = screen_name
		loguser.iconaddress = profile_image_url
		# loguser.logpassword = "wutong"
		loguser.save()
		return redirect(action_url)
	except:
		raise Http404("Somthing Wrong")


@login_required(login_url='/user/loggin/')
def weixinconnection(request):
	try:
		action_url = reverse("user_detailinformations", kwargs={"user_id": request.user.id})
		CODE = request.GET.get('code')
		url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx59a3f67caac61d02&secret=25fdbdc3e5ae5327111c97bba099ba28&code="+CODE+"&grant_type=authorization_code"
		req = urllib2.Request(url)
		res_data = urllib2.urlopen(req)
		res = res_data.readline()
		test = json.loads(res)['refresh_token']
		refreshurl = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=wx59a3f67caac61d02&grant_type=refresh_token&refresh_token="+str(test)
		rereq = urllib2.Request(refreshurl)
		reres_data = urllib2.urlopen(rereq)
		reres = reres_data.readline()
		access_token = json.loads(reres)['access_token']
		openid = json.loads(reres)['openid']
		authurl = "https://api.weixin.qq.com/sns/auth?access_token="+str(access_token)+"&openid="+str(openid)
		authreq = urllib2.Request(authurl)
		authres_data = urllib2.urlopen(authreq)
		authres = authres_data.readline()
		errmsg = json.loads(authres)['errmsg']
		if str(errmsg) == "ok":
			pass;
		else:
			return redirect(action_url)
		infourl = "https://api.weixin.qq.com/sns/userinfo?access_token="+str(access_token)+"&openid="+str(openid)
		inforeq = urllib2.Request(infourl)
		infores_data = urllib2.urlopen(inforeq)
		infores = infores_data.readline()
		nickname = str(json.loads(infores)['nickname'])
		headimgurl = str(json.loads(infores)['headimgurl'])
		unionid = str(json.loads(infores)['unionid'])
		try:
			weixinuser = WeixinUser.objects.get(weixinid = unionid)
			isweixinuser = True
		except:
			isweixinuser = False
		if isweixinuser:
			raise Http404("微信帐号已经关联别的帐号")
		else:
			pass
		loguser = WeixinUser()
		loguser.user = request.user
		loguser.weixinid = unionid
		loguser.weixinname = nickname
		loguser.iconaddress = headimgurl
		# loguser.logpassword = "wutong"
		loguser.save()
		return redirect(action_url)
	except :
		raise Http404("Somthing Wrong")

def disweixinconnection(request):
	try:
		action_url = reverse("user_detailinformations", kwargs={"user_id": request.user.id})
		weixinuser = WeixinUser.objects.get(user = request.user)
		weixinuser.delete()
		return redirect(action_url)
	except:
		raise Http404("Somthing Wrong")

def disweiboconnection(request):
	try:
		action_url = reverse("user_detailinformations", kwargs={"user_id": request.user.id})
		weibouser = WeiboUser.objects.get(user = request.user)
		weibouser.delete()
		return redirect(action_url)
	except:
		raise Http404("Somthing Wrong")


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
		notifications = Notification.objects.filter(recipient = user).exclude(verb = '_@_').order_by("-timestamp")
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
		timeline = Notification.objects.get(id = 1029).timestamp
		context = {
			'userofinfor': user,
			"notifications": contacts,
			'host': host,
			'hostname': hostname,
			'timeline': timeline,
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

		if request.method == 'POST' and request.POST.get('privcycomment', False) and request.POST.get('privcytarget', False):
			text = request.POST.get('privcycomment')
			targetid = int(request.POST.get('privcytarget'))
			targetuser = MyUser.objects.get(id = targetid)
			try:
				# c = Comment(user=user, is_privcycomment=True, text=text)
				notify.send(sender=sender, target_object=None, recipient = targetuser, verb="_@_", text=text)
				cachekey = "user_unread_count" + str(targetuser.id)
				if cache.get(cachekey) != None:
					cache.incr(cachekey)
				else:
					unread = Notification.objects.filter(recipient = targetuser).filter(read = False).count()
					cache.set(cachekey,  unread, settings.CACHE_EXPIRETIME)	
				cachekey = "user_privcyunread_count" + str(targetuser.id)
				if cache.get(cachekey) != None:
					cache.incr(cachekey)
				else:
					unread = Notification.objects.filter(recipient = user).filter(read = False).filter(verb = '_@_').count()
					cache.set(cachekey,  unread, settings.CACHE_EXPIRETIME)	


			except:
				traceback.print_exc()
			return redirect(request.get_full_path())

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
		request.session['lastpage'] = request.get_full_path()
		context = {
			'topic' : contacts,
			'host': host,
			'userofinfor': user,
			'hostname': hostname,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_userdashboardarticletopic.html',  context)

#我的试用
def userdashboardtry(request, user_id):
	try:
		user = MyUser.objects.get(pk=user_id)
		sender = request.user
		if user == sender:
			host = True
			hostname = '我的'
		else:
			host = False
			hostname = '他的'
		application = Application.objects.filter(user = user).order_by("-id")
		# 分页
		paginator = Paginator(application, 10)
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
			'application' : contacts,
			'host': host,
			'userofinfor': user,
			'hostname': hostname,
			}
	except MyUser.DoesNotExist:
		raise Http404("MyUser does not exist")
	return render(request, 'user_detailtry.html',  context)



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

		if instancetype == 'Topic':
			cachekey = "topic_user_count_" + str(request.user.id)
			if cache.get(cachekey) != None:
				cache.decr(cachekey)
			else:
				usertopicnum = Topic.objects.filter(writer = request.user).count()
				cache.set(cachekey,  usertopicnum)		


		if instancetype == 'Comment':
			cachekey = "comment_user_count_" + str(request.user.id)
			if cache.get(cachekey) != None:
				cache.decr(cachekey)
			else:
				usercomnum = Comment.objects.filter(user = request.user).count()
				cache.set(cachekey,  usercomnum)

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
			if cache.get(cachekey) < 0:
				cache.set(cachekey, 0, settings.CACHE_EXPIRETIME)
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


def notificationsconversation(request):
	if request.is_ajax():
		targetid = request.POST.get('privcytargetid')
		recipient = MyUser.objects.get(id = targetid)

		notifications1 = Notification.objects.filter(recipient = recipient).filter(sender_object = request.user).filter(verb = '_@_')
		notifications2 = Notification.objects.filter(recipient = request.user).filter(sender_object = recipient).filter(verb = '_@_')
		notifications = notifications1|notifications2.order_by('-id')
		test = []
		test2 = []
		test3 = []
		for item in notifications:
			text = item.sender_object.username+' : '+item.text
			beijingtime = item.timestamp + datetime.timedelta(hours=8) 
			time = beijingtime.strftime('%Y.%m.%d %H:%M')
			if item.sender_object == request.user:
				backcolor = 'backgreen'	
			else:
				backcolor = 'backwhite'	
			test.append(text);  
			test2.append(time);
			test3.append(backcolor);
		data = {
			"notifications": test,
			"notificationstime": test2,
			"backcolor": test3,
			}
		json_data = json.dumps(data)
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404





def repassword(request):
	form = RepasswordForm(request.GET or None)
	next_url = request.GET.get('next')
	action_url = reverse("repassword")
	if form.is_valid():
		human = True
		username = form.cleaned_data['username']
		phonenumber = form.cleaned_data['phonenumber']
		try:
			user = MyUser.objects.get(username=username, phonenumber=phonenumber)
		except MyUser.DoesNotExist:
			user = None
		if 	user:
			new_repassworduser = Repassworduser(username = username, userid = user.id, phonenumber = phonenumber)
			new_repassworduser.save()
			user.set_password('wutong')
			user.save()
			text = username + '申请重置密码，手机号：' + phonenumber + '，用户id：'+ str(user.id) + '，新密码:wutong。'
			recipient = MyUser.objects.get(id = 519)
			try:
				# c = Comment(user=user, is_privcycomment=True, text=text)
				notify.send(sender=user, target_object=None, recipient = recipient, verb="_@_", text=text)
				cachekey = "user_unread_count" + str(recipient.id)
				if cache.get(cachekey) != None:
					cache.incr(cachekey)
				else:
					unread = Notification.objects.filter(recipient = recipient).filter(read = False).count()
					cache.set(cachekey,  unread, settings.CACHE_EXPIRETIME)	
			except:
				traceback.print_exc()
			return render(request, 'builtsucss.html')
		else:
			messages.error(request, '输入信息错误，请重新输入！')
	context = {
		"form": form,
		"action_url": action_url,
		"submit_btn": "提交",
		}
	return render(request, 'repassword.html',  context)

