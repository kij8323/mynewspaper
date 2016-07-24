#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import Company, CollectionCompany
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


def company_detail(request, company_id):
	company = Company.objects.get(pk=company_id)
	firm_article = company.article_set.all
	user = request.user
	sharelink = request.get_host()+request.get_full_path()
	if company.financing == '其它'.encode('utf-8'):
		financing_show = False
	else :
		financing_show = True
	collection = CollectionCompany.objects.filter(company=company, user=user.id)
	if collection: 
		collection = '已收藏'
		collection_icon = 'glyphicon-star'
	else:
		collection = '收藏'
		collection_icon = 'glyphicon-star-empty'
	context = {
		'company' : company,
		'firm_article' : firm_article,
		'financing_show': financing_show,
		'collection': collection,
		"collection_icon": collection_icon,
		'sharelink': sharelink,
	}
	return render(request, 'company_detail.html', context)

def company_list(request):
	company = Company.objects.all().filter(verify = True).order_by('-id')
		# 分页
	paginator = Paginator(company, 15)
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
	}
	return render(request, 'company_list.html', context)

def company_content_fresh(request):
	if request.session.get('firm-industry', False):
		industry = request.session['firm-industry'].encode('utf-8')
	if request.session.get('firm-financing', False):
		financing = request.session['firm-financing'].encode('utf-8')
	if request.session.get('firm-locationx', False):
		locationx = request.session['firm-locationx'].encode('utf-8')
	if industry == '全部'.encode('utf-8'):
		# industry = ('智能家居','可穿戴设备', '智能健康','智能配件', '智能母婴设备'
		# 			,'机器人', '无人机','手机平板', 'VR/AR','智能交通', '其它')
		#companylist = Company.objects.filter(industry__in=industry)
		companylist = Company.objects.all()
	else :
		companylist = Company.objects.filter(industry=industry)
	if financing == '全部'.encode('utf-8'):
		# financing = ('未融资', '种子轮','天使轮', 'Pre-A','A轮', 'B轮'
		# 			,'C轮', 'D轮及以上','其它')			
		#companylist = companylist.filter(financing__in=financing)
		companylist = companylist
	else :
		companylist = companylist.filter(financing=financing)
	if locationx == '全部'.encode('utf-8'):
		# locationx = ('北京市', '上海市','天津市', '重庆市','深圳市', '四川省'
		# 			,'广东省', '其它')	
		#companylist = companylist.filter(location__in=locationx)
		companylist = companylist
	else :
		companylist = companylist.filter(location=locationx)
	companylist = companylist.filter(verify=True).order_by('-id')		
	paginator = Paginator(companylist, 15)
	#page = request.GET.get('page')
	page = request.session.get('list_page', False)
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
	# If page is not an integer, deliver first page.
		contacts = paginator.page(1)
	except EmptyPage:
	# If page is out of range (e.g. 9999), deliver last page of results.
		contacts = paginator.page(paginator.num_pages)
	context = {
		"company": contacts,
	}
	return render(request, 'company_content_fresh.html',  context)

def company_list_fresh(request):
	if request.is_ajax():
		request.session['firm-industry'] = request.GET.get('industry')
		request.session['firm-financing'] = request.GET.get('financing')
		request.session['firm-locationx'] = request.GET.get('locationx')
		request.session['list_page'] = request.GET.get('list_page')
		data = {
			"test": 'ok',
		}
		json_data = json.dumps(data)
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404

@login_required  
def company_built1(request):
	if request.method == 'POST':
		company = Company()
		company.title = request.POST.get('company_title')
		company.weburl = request.POST.get('company_weburl')
		company.uper = request.user
		company.save()
		request.session['company_id'] = company.id
		return redirect('company_built2')
	else:
		return render(request, 'company_built1.html')

@login_required  
def company_built2(request):
	if request.session.get('company_id', False):
		company_id = request.session['company_id']
		company = Company.objects.get(pk=company_id)
		if request.method == 'POST' and request.FILES.get('img', False):
			image = request.FILES['img']
			company.logo = image
			company.save() 
			os.system('echo yes | python /home/shen/Documents/paperproject/mynewspaper/manage.py collectstatic')
			return redirect('company_built2')
		if request.method == 'POST':
			if request.POST.get('company_location') == '0':
				company.location = "北京市".encode('utf-8')
			elif request.POST.get('company_location') == '1':
				company.location = "上海市".encode('utf-8')
			elif request.POST.get('company_location') == '2':
				company.location = "天津市".encode('utf-8')
			elif request.POST.get('company_location') == '3':
				company.location = "重庆市".encode('utf-8')
			elif request.POST.get('company_location') == '4':
				company.location = "深圳市".encode('utf-8')
			elif request.POST.get('company_location') == '5':
				company.location = "四川省".encode('utf-8')
			elif request.POST.get('company_location') == '6':
				company.location = "广东省".encode('utf-8')
			elif request.POST.get('company_location') == '7':
				company.location = "其它".encode('utf-8')
			if request.POST.get('company_industry') == '0':
				company.industry = "智能家居".encode('utf-8')
			elif request.POST.get('company_industry') == '1':
				company.industry = "可穿戴设备".encode('utf-8')
			elif request.POST.get('company_industry') == '2':
				company.industry = "智能健康".encode('utf-8')
			elif request.POST.get('company_industry') == '3':
				company.industry = "智能配件".encode('utf-8')
			elif request.POST.get('company_industry') == '4':
				company.industry = "智能母婴设备".encode('utf-8')
			elif request.POST.get('company_industry') == '5':
				company.industry = "机器人".encode('utf-8')
			elif request.POST.get('company_industry') == '6':
				company.industry = "无人机".encode('utf-8')
			elif request.POST.get('company_industry') == '7':
				company.industry = "手机平板".encode('utf-8')
			elif request.POST.get('company_industry') == '8':
				company.industry = "VR/AR".encode('utf-8')
			elif request.POST.get('company_industry') == '9':
				company.industry = "智能交通".encode('utf-8')
			elif request.POST.get('company_industry') == '10':
				company.industry = "其它".encode('utf-8')
			company.associatetitle = request.POST.get('company_associatetitle')
			company.product = request.POST.get('company_product')
			company.client = request.POST.get('company_client')
			company.financing = '其它'.encode('utf-8')
			company.save()
			return redirect('builtsucss')
		context = {
			'company' : company,
			'company_title' : company.title,
		}
		return render(request, 'company_built2.html', context)
	else:
		return render(request, 'company_built1.html')

@login_required  
def company_built3(request, company_id):
	user = Company.objects.get(id = company_id).uper
	sender = request.user
	if user == sender:
		company = Company.objects.get(pk=company_id)
		action_url = reverse("company_built3", kwargs={"company_id": company_id})
		if request.method == 'POST' and request.FILES.get('img', False):
			image = request.FILES['img']
			company.logo = image
			company.save() 
			os.system('echo yes | python /home/shen/Documents/paperproject/mynewspaper/manage.py collectstatic')
			return redirect(action_url)
		if request.method == 'POST' and request.FILES.get('img1', False):
			image = request.FILES['img1']
			company.images1 = image
			company.save() 
			os.system('echo yes | python /home/shen/Documents/paperproject/mynewspaper/manage.py collectstatic')
			return redirect(action_url)
		if request.method == 'POST' and request.FILES.get('img2', False):
			image = request.FILES['img2']
			company.images2 = image
			company.save() 
			os.system('echo yes | python /home/shen/Documents/paperproject/mynewspaper/manage.py collectstatic')
			return redirect(action_url)
		if request.method == 'POST' and request.FILES.get('img3', False):
			image = request.FILES['img3']
			company.images3 = image
			company.save() 
			os.system('echo yes | python /home/shen/Documents/paperproject/mynewspaper/manage.py collectstatic')
			return redirect(action_url)
		if request.method == 'POST':
			if request.POST.get('company_associatetitle') == '':
				pass
			else:
				company.associatetitle = request.POST.get('company_associatetitle')
			if request.POST.get('company_product') == '':
				pass
			else:
				company.product = request.POST.get('company_product')
			if request.POST.get('company_client') == '':
				pass
			else:
				company.client = request.POST.get('company_client')
			if request.POST.get('select_pastfinancing') == '0':
				company.financing = "未融资".encode('utf-8')
			elif request.POST.get('select_pastfinancing') == '1':
				company.financing = "种子轮".encode('utf-8')
			elif request.POST.get('select_pastfinancing') == '2':
				company.financing = "天使轮".encode('utf-8')
			elif request.POST.get('select_pastfinancing') == '3':
				company.financing = "Pre-A".encode('utf-8')
			elif request.POST.get('select_pastfinancing') == '4':
				company.financing = "A轮".encode('utf-8')
			elif request.POST.get('select_pastfinancing') == '5':
				company.financing = "B轮".encode('utf-8')
			elif request.POST.get('select_pastfinancing') == '6':
				company.financing = "C轮".encode('utf-8')
			elif request.POST.get('select_pastfinancing') == '7':
				company.financing = "D轮及以上".encode('utf-8')
			elif request.POST.get('select_pastfinancing') == '8':
				company.financing = "其它".encode('utf-8')
			company.sameproduct = request.POST.get('company_sameproduct')
			company.qita = request.POST.get('company_qita')
			company.team = request.POST.get('company_team')
			company.pastfinancing = request.POST.get('company_pastfinancing')
			company.save()
			return redirect('builtsucss')
		context = {
			'company' : company,
		}
		return render(request, 'company_built3.html', context)
	else:
		raise Http404

def builtsucss(request):
	return render(request, 'builtsucss.html')

from django.core.cache import cache
#收藏话题
def collectioncompany(request):
	try:
		companyid = request.POST.get('companyid')
		company = Company.objects.get(pk=companyid)
		user = request.user
	except Company.DoesNotExist:
		raise Http404("Company does not exist")
	collection = CollectionCompany.objects.filter(company=company, user=user)
	cachekey = "company_collection_" + str(companyid)
	if collection: 
		collection.delete()
		collecicon = '收藏'
		collection_icon = 'glyphicon-star-empty'
		if cache.get(cachekey) != None:
			cache.decr(cachekey)
		else:
			company = Company.objects.get(id=value)
			cache.set(cachekey,  company.collectioncompany_set.count(), 1209600)
	else:
		c = CollectionCompany(user=user, company=company)
		c.save()
		collecicon = '已收藏'
		collection_icon = 'glyphicon-star'
		if cache.get(cachekey) != None:
			cache.incr(cachekey)
		else:
			company = Company.objects.get(id=value)
			cache.set(cachekey,  company.collectioncompany_set.count(), 1209600)
	data = {
	 'collecicon': collecicon,
	 'collection_icon': collection_icon,
	 'collectioncount': cache.get(cachekey),
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')

