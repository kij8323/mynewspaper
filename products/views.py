#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from .models import Products, Application
from notifications.atwho import atwho
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from comment.models import Comment, CommentLike, CommentDisLike
from django.core.cache import cache
import json
from accounts.models import MyUser
from article.tasks import readersin, add, readersout, instancedelete, instancesave
from django.conf import settings
import traceback  
from django.http import Http404
from article.form import CommentForm
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.core.urlresolvers import reverse

def productsall(request):
	products = Products.objects.order_by('-id')
	paginator = Paginator(products, 15)
	page = request.GET.get('page')
	#把本页地址装入session
	request.session['lastpage'] = request.get_full_path()
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
	# If page is not an integer, deliver first page.
		contacts = paginator.page(1)
	except EmptyPage:
	# If page is out of range (e.g. 9999), deliver last page of results.
		contacts = paginator.page(paginator.num_pages)
	pagerange = contacts.paginator.page_range
	last_page = contacts.paginator.page_range[-1]
	if contacts.paginator.page_range[-1] > 8 and contacts.number<=5:
		pagerange = range(1,8) 
		ellipsis_front = False
		ellipsis_real = True
	elif contacts.paginator.page_range[-1] > 8 and contacts.number+4>contacts.paginator.page_range[-1] and contacts.number>5:
		pagerange = range(contacts.paginator.page_range[-1]-6, contacts.paginator.page_range[-1]+1)
		ellipsis_front = True
		ellipsis_real = False
	elif contacts.paginator.page_range[-1] > 8 and contacts.number+4<=contacts.paginator.page_range[-1] and contacts.number>5:
		pagerange = range(contacts.number-3, contacts.number+4)
		ellipsis_front = True
		ellipsis_real = True
	else:
		ellipsis_front = False
		ellipsis_real = False
	context = {
		"products":contacts,
		'pagerange': pagerange,
		'ellipsis_front': ellipsis_front,
		'ellipsis_real': ellipsis_real,
		'last_page': last_page,
	}
	return render(request, 'productsall.html',  context)


def products_detail(request, products_id):
	try:
		products = Products.objects.get(pk=products_id)
	except products.DoesNotExist:
		raise Http404("Products does not exist")
	user = request.user
	if request.method == 'POST' and user.is_authenticated:
		user.phonenumber = request.POST.get('phonenumberinput')
		user.address = request.POST.get('addressinput')
		user.save()
		news_App = Application(user=user, products=products)
		news_App.save()
		cachekey = "products_applyamount_" + str(products_id)
		if cache.get(cachekey) != None:
			cache.incr(cachekey)
		else:
			cache.set(cachekey, Application.objects.filter(products=products).count(), settings.CACHE_EXPIRETIME)
		return redirect(reverse("products_detail", kwargs={"products_id": products_id}))
	else:
		try:
			application = Application.objects.get(user=user.id, products=products)
			applybutton = True
		except Application.DoesNotExist:
			applybutton = False
		# if application:
		# 	applybutton = True
		# else:
		# 	applybutton = False
		comment = Comment.objects.filter(products=products).order_by('-timestamp')
		if comment.count() > 5:
			moercomment = True
		else:
			moercomment = False#链接最热回复和按时间排序的回复
		comment = comment[:5]
		#把本页地址装入session
		request.session['lastpage'] = request.get_full_path()
		#分享链接的地址
		sharelink = request.get_host()+request.get_full_path()
		# applyamount = Application.objects.filter(products=products).count()
		hotry = Products.objects.filter(status = 1).exclude(id = products_id).order_by('-id')[0:5]

		context = {
			"products":products,
			"comment": comment,
			"form": CommentForm,
			'sharelink': sharelink,
			'moercomment': moercomment,
			'user':user,
			'applybutton':applybutton,
			# 'applyamount':applyamount,
			'hotry':hotry,
		}
		return render(request, 'products_detail.html',  context)

def productsapply(request, products_id):
	try:
		products = Products.objects.get(pk=products_id)
	except products.DoesNotExist:
		raise Http404("Products does not exist")
	user = request.user
	if request.method == 'POST' and user.is_authenticated:
		user.phonenumber = request.POST.get('phonenumberinput')
		user.address = request.POST.get('addressinput')
		user.save()
		news_App = Application(user=user, products=products)
		news_App.save()
		cachekey = "products_applyamount_" + str(products_id)
		if cache.get(cachekey) != None:
			cache.incr(cachekey)
		else:
			cache.set(cachekey, Application.objects.filter(products=products).count(), settings.CACHE_EXPIRETIME)
		return redirect(reverse("products_detail", kwargs={"products_id": products_id}))
	else:
		try:
			application = Application.objects.get(user=user.id, products=products)
			applybutton = True
		except Application.DoesNotExist:
			applybutton = False
		# if application:
		# 	applybutton = True
		# else:
		# 	applybutton = False
		#把本页地址装入session
		request.session['lastpage'] = request.get_full_path()
		#分享链接的地址
		sharelink = request.get_host()+request.get_full_path()
		# applyamount = Application.objects.filter(products=products).count()
		hotry = Products.objects.filter(status = 1).exclude(id = products_id).order_by('-id')[0:5]
		#申请名单
		applicationlist = Application.objects.filter(products=products)
		#中奖名单
		applicationlistsucss = Application.objects.filter(products=products).filter(verify=True)
		context = {
			"products":products,
			"form": CommentForm,
			'sharelink': sharelink,
			'user':user,
			'applybutton':applybutton,
			# 'applyamount':applyamount,
			'hotry':hotry,
			'applicationlist':applicationlist,
			'applicationlistsucss':applicationlistsucss,
		}
		return render(request, 'products_apply.html',  context)

#ajax，文章评论
def productscomment(request):
	if request.is_ajax() and request.method == 'POST':
		text = request.POST.get('comment')#评论的内容
		productsid = request.POST.get('productsid')
		products = Products.objects.get(pk=productsid)
		user = request.user
		print 'test'
		try:
			c = Comment(user=user, products=products, text=text)
			c.save()
			#文章回复数量redis缓存 增加1
			cachekey = "products_comment_" + str(productsid)
			if cache.get(cachekey) != None:
				cache.incr(cachekey)
			else:
				cache.set(cachekey, products.comment_set.count(), settings.CACHE_EXPIRETIME)
			#返回@用户的列表，并向@的用户发送消息
			userlist = atwho(text = text, sender = user, targetcomment = None, targetarticle = None
							, targetproducts = products, targetopic = None)
			#给被@的用户增加链接
			for item in userlist:
				atwhouser = MyUser.objects.get(username = item)
				test = "@<a href='" +'/user/'+str(atwhouser.id)+'/informations/'+"'>"+atwhouser.username+"</a>"+' '
				test1 = "@<a href='" +'/user/'+str(atwhouser.id)+'/informations/'+"'>"+atwhouser.username+"</a>"+'&nbsp;'
				text = text.replace('@'+item+' ', test);
				text = text.replace('@'+item+'&nbsp;', test1);
			data = {
			"user": user.username,
			"text": text,
			"commentid": c.id
			}
			json_data = json.dumps(data)
			return HttpResponse(json_data, content_type='application/json')
		except:
			traceback.print_exc()
			raise Http404(traceback)
	else:
		raise Http404


#ajax，评论的评论
def productscommentcomment(request):
	if request.is_ajax() and request.method == 'POST':
		print 'commentcomment'
		text = request.POST.get('comment')
		productsid = request.POST.get('productsid')
		#parenttext = request.POST.get('parenttext')
		preentid = request.POST.get('preentid')
		products = Products.objects.get(pk=productsid)
		#comment = Comment.objects.filter(products=products)
		targetcomment = Comment.objects.get(pk=preentid)
		user = request.user
		try:
			c = Comment(user=user, products=products, text=text, parent=targetcomment)
			c.save()
			#文章回复数量缓存 增加1
			cachekey = "products_comment_" + str(productsid)
			if cache.get(cachekey) != None:
				cache.incr(cachekey)
			else:
				cache.set(cachekey, products.comment_set.count(), settings.CACHE_EXPIRETIME)
			#被评论的评论readers+1放到消息队列中
			readersin.delay(targetcomment)
			#返回@用户的列表，并向@的用户发送消息
			userlist = atwho(text = text, sender = user, targetcomment = targetcomment, targetarticle = None
							, targetproducts = products, targetopic = None )
			#给被@的用户增加链接
			for item in userlist:
				print 'for item in userlist:'
				atwhouser = MyUser.objects.get(username = item)
				test = "@<a href='" +'/user/'+str(atwhouser.id)+'/informations/'+"'>"+atwhouser.username+"</a>"+' '
				text = text.replace('@'+item+' ', test);
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

#显示更多评论按钮
def productsmorecomment(request):
	try:
		productsid = request.POST.get('productsid')
		products = Products.objects.get(pk=productsid)
		comment = Comment.objects.filter(products=products)
	except products.DoesNotExist:
		raise Http404("products does not exist")
	if request.is_ajax():
		request.session['commentlen'] = request.POST.get('commentlen')
	if comment.count() == int(request.session['commentlen']):
		loadcompleted = '已全部加载完成'
	else:
		loadcompleted = '点击加载更多'
	data = {
		'loadcompleted' : loadcompleted
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


#加载更多评论的页面
def productscommentpage(request, products_id):
	try:
		products = Products.objects.get(pk=products_id)
		comment = Comment.objects.filter(products=products)
	except products.DoesNotExist:
		raise Http404("products does not exist")
	if request.session.get('commentlen', False):
		commentlen = request.session['commentlen']
	commentlen = int(commentlen)
	comment = comment[commentlen:commentlen+5]
	context = {
		"comment": comment,
	}
	return render(request, 'commentpage.html',  context)
