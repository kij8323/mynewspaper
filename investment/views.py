#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import Investment, CollectionInvestment, InvestmentBuiltForm
from django.shortcuts import render, HttpResponseRedirect, redirect
import os
from django.contrib.auth.decorators import login_required  
import json
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import Http404
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# Create your views here.

def investment_list_index(request):
	investment = Investment.objects.all().order_by('-investindex')
	paginator = Paginator(investment, 20)
	page = request.GET.get('page')
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
		"investment": contacts,
		'pagerange': pagerange,
		'ellipsis_front': ellipsis_front,
		'ellipsis_real': ellipsis_real,
		'last_page': last_page,
	}
	return render(request, 'investment_list_index.html',  context)

def investment_list_id(request):
	investment = Investment.objects.all().order_by('-id')
	paginator = Paginator(investment, 20)
	page = request.GET.get('page')
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
		"investment": contacts,
		'pagerange': pagerange,
		'ellipsis_front': ellipsis_front,
		'ellipsis_real': ellipsis_real,
		'last_page': last_page,
	}
	return render(request, 'investment_list_id.html',  context)

def investment_detail(request, investment_id):
	investment = Investment.objects.get(pk=investment_id)
	user = request.user
	collection = CollectionInvestment.objects.filter(investment=investment, user=user.id)
	if collection: 
		collection = '已收藏'
		collection_icon = 'glyphicon-star'
	else:
		collection = '收藏'
		collection_icon = 'glyphicon-star-empty'
	investment_article = investment.article_set.all
	context = {
		'investment': investment,
		'collection': collection,
		'collection_icon': collection_icon,
		'investment_article': investment_article,
	}
	return render(request, 'investment_detail.html', context)

from django.core.cache import cache
#收藏话题
def collectioninvestment(request):
	try:
		investmentid = request.POST.get('investmentid')
		investment = Investment.objects.get(pk=investmentid)
		user = request.user
	except investment.DoesNotExist:
		raise Http404("investment does not exist")
	collection = CollectionInvestment.objects.filter(investment=investment, user=user)
	cachekey = "investment_collection_" + str(investmentid)
	if collection: 
		collection.delete()
		collecicon = '收藏'
		collection_icon = 'glyphicon-star-empty'
		if cache.get(cachekey) != None:
			cache.decr(cachekey)
		else:
			cache.set(cachekey,  investment.collectioninvestment_set.count(), 1209600)
	else:
		c = CollectionInvestment(user=user, investment=investment)
		c.save()
		collecicon = '已收藏'
		collection_icon = 'glyphicon-star'
		if cache.get(cachekey) != None:
			cache.incr(cachekey)
		else:
			cache.set(cachekey,  investment.collectioninvestment_set.count(), 1209600)
	data = {
	 'collecicon': collecicon,
	 'collection_icon': collection_icon,
	 'collectioncount': cache.get(cachekey),
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')

def investmentbuilt(request):
	if request.method == 'POST':
		q = Investment(title=request.POST.get('investment_title'),
					 weburl=request.POST.get('investment_weburl'),
					 fundtime=request.POST.get('investment_fundtime'),
					 investindex=int(request.POST.get('investment_investindex')),
					 introduce=request.POST.get('investment_introduce'),
					 preference1=request.POST.get('investment_preference1'),
					 preference2=request.POST.get('investment_preference2'),
					 preference3=request.POST.get('investment_preference3'),
					 preference4=request.POST.get('investment_preference4'),
					 preference5=request.POST.get('investment_preference5'),
					 investfiled1=request.POST.get('investment_investfiled1'),
					 investfiled2=request.POST.get('investment_investfiled2'),
					 investfiled3=request.POST.get('investment_investfiled3'),
					 investfiled4=request.POST.get('investment_investfiled4'),
					 investfiled5=request.POST.get('investment_investfiled5'),
					 investfiled6=request.POST.get('investment_investfiled6'),
					 investfiled7=request.POST.get('investment_investfiled7'),
					 investfiled8=request.POST.get('investment_investfiled8'),
					 investfiled9=request.POST.get('investment_investfiled9'),
					 #logo = request.FILES.get('img'),
					 	)
		q.save()
		print 'image'
		if  request.FILES.get('img', False):
			image = request.FILES['img']
			print image
			q.logo = image
			q.save() 
			os.system('echo yes | python /home/shen/Documents/paperproject/mynewspaper/manage.py collectstatic')
		return redirect('investment_list_id')
	else:

		return render(request, 'investmentbuilt.html')

