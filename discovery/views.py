#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Discovery, Discoveryhost

from bs4 import BeautifulSoup
import json
from django.http import HttpResponse
import traceback
import sys  
import re
import time
from selenium import webdriver
from django.db import connection
from django.db.utils import OperationalError

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



reload(sys)  
sys.setdefaultencoding('utf8')   
from article.tasks import instancesave

def discovery(request):
	jiguo = Discoveryhost.objects.get(id = 1)
	discovery = Discovery.objects.all().filter(verify = True).order_by('-id')[0:8]
	discoveryhost = Discoveryhost.objects.all()
	context = {
		"discovery":discovery,
		"jiguo":jiguo,
		"discoveryhost":discoveryhost,
	}
	return render(request, 'discovery.html',  context)




def discoverycategory(request, category_id):
	jiguo = Discoveryhost.objects.get(id = 1)
	discovery = Discovery.objects.all().filter(verify = True).filter(host = category_id).order_by('-id')[0:8]
	discoveryhost = Discoveryhost.objects.all()
	context = {
		"discovery":discovery,
		"discoveryhost":discoveryhost,
		"jiguo":jiguo,
		"category_id":category_id,
	}
	return render(request, 'discoverycategory.html',  context)




def morediscoverycategory(request):
	if request.is_ajax():
		request.session['discoverylen'] = request.POST.get('discoverylen')
		discoverylen = int(request.session['discoverylen'])
		request.session['category_id'] = request.POST.get('category_id')
		category_id = int(request.session['category_id'])
		discoveryquery = Discovery.objects.filter(host = category_id).filter(verify = True).order_by('-id')
	if discoveryquery.count() == discoverylen:
		loadcompleted = '已全部加载完成'
	else:
		loadcompleted = '加载更多'
	data = {
		"loadcompleted": loadcompleted,
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def discoverycategorypage(request):
	if request.session.get('discoverylen', False):
		discoverylen = request.session['discoverylen']
	if request.session.get('category_id', False):
		category_id = int(request.session['category_id'])
	discoveryquery = Discovery.objects.filter(host = category_id).filter(verify = True).order_by('-id')
	discoverylen = int(discoverylen)
	discoveryquery = discoveryquery[discoverylen:discoverylen+4]
	context = {
		"discovery": discoveryquery,
	}
	return render(request, 'discoverycategorypage.html',  context)















def morediscovery(request):
	if request.is_ajax():
		request.session['discoverylen'] = request.POST.get('discoverylen')
		discoverylen = int(request.session['discoverylen'])
		discoveryquery = Discovery.objects.filter(verify = True).order_by('-id')
	if discoveryquery.count() == discoverylen:
		loadcompleted = '已全部加载完成'
	else:
		loadcompleted = '加载更多'
	data = {
		"loadcompleted": loadcompleted,
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def discoverypage(request):
	if request.session.get('discoverylen', False):
		discoverylen = request.session['discoverylen']
	discoveryquery = Discovery.objects.filter(verify = True).order_by('-id')
	discoverylen = int(discoverylen)
	discoveryquery = discoveryquery[discoverylen:discoverylen+4]
	context = {
		"discovery": discoveryquery,
	}
	return render(request, 'discoverypage.html',  context)



def discoveryjiguo(request):
	discoveryhost = Discoveryhost.objects.get(id = 1)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://www.jiguo.com/event/freelist.html'
	try:
		driver.get(urlpage)
		time.sleep(2)
		driver.find_element_by_xpath("//li//a[@data-type='open']").click()
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.event-class-list ul li')
		discovery.reverse()
		for item in discovery:
			url = 'http://www.jiguo.com/' + str(item.select(' a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try: 
					title = str(item.select('.e-title')[0].get_text())
					amount = str(item.select('.e-item-hide-cell  .gray')[0].get_text())
					img = str(item.select('a img')[0].attrs['src'])
					price = str(item.select('.e-item-hide-cell  .fr')[1].get_text())
					infor = '免费试用'
					count = str(item.select('.e-query  span')[0].get_text())
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass
	driver.close()
	time.sleep(2)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://www.jiguo.com/event/paylist.html'
	try:
		driver.get(urlpage)
		time.sleep(2)
		driver.find_element_by_xpath("//li//a[@data-type='open']").click()
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.event-class-list ul li')
		discovery.reverse()
		for item in discovery:
			url = 'http://www.jiguo.com/' + str(item.select(' a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try: 
					title = str(item.select('.e-title')[0].get_text())
					amount = str(item.select('.e-item-hide-cell  .gray')[0].get_text())
					img = str(item.select('a img')[0].attrs['src'])
					price = str(item.select('.e-item-hide-cell  .fr')[2].get_text())
					infor = '折扣试用'
					count = str(item.select('.e-query  span')[0].get_text())
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass
	driver.close()

	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def discoveryairanshao(request):
	discoveryhost = Discoveryhost.objects.get(id = 16)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://iranshao.com/trials?cat=in_apply'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.trial-list-item.in-apply')
		discovery.reverse()
		for item in discovery:
			url = 'http://iranshao.com/trials/' + str(item.attrs['data-id'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try: 
					title = str(item.select('.title')[0].get_text())
					amount = str(item.select('.quantity')[0].get_text())
					img = str(item.select('.img-container')[0].attrs['style'])[23:-2]
					price = str(item.select('.price')[0].get_text())
					infor = '免费众测'
					count = str(item.select('.content-container span')[1].get_text())
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass
	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')





def discoveryjuyoufan(request):
	discoveryhost = Discoveryhost.objects.get(id = 17)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://try.pchouse.com.cn/'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.pic-txt.pic-txtb')
		discovery.reverse()
		for item in discovery:
			url = str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try: 
					btn = str(item.select('.btn.btn-1')[0].get_text())
					title = str(item.select('.txt-area dt')[0].get_text())
					amount = str(item.select('.txt-area .provide')[0].get_text())
					img = 'http://www.wutongnews.com/static/media/images/usericon/juyoufan.jpg'
					price = str(item.select('.txt-area .price')[0].get_text())
					infor = '免费众测'
					count = str(item.select('.count-down.count-downa')[0].get_text())
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass
	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def discoverytengxuncar(request):
	discoveryhost = Discoveryhost.objects.get(id = 18)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://zc.chezhuka.qq.com/web/act/list'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.J_MainCont.main-cont-item')
		discovery.reverse()
		for item in discovery:
			url = 'http://zc.chezhuka.qq.com' + str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try: 
					title = str(item.select('.right h3')[0].get_text()).replace(' ','').replace('\n','')
					amount = str(item.select('.g-block-top .br1')[1].get_text()).replace(' ','').replace('\n','')
					img = str(item.select('a img')[0].attrs['src'])
					price = str(item.select('.g-block-top li')[2].get_text()).replace(' ','').replace('\n','')
					infor = '免费众测'
					count = '申请中'
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass
	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')





def discoverysmzdm(request):
	discoveryhost = Discoveryhost.objects.get(id = 19)
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = 'User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
	dcap["phantomjs.page.settings.loadImages"] = False
	driver = webdriver.PhantomJS(desired_capabilities=dcap)
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'https://test.smzdm.com/shenqing/'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.list_test.list_testProduct li')
		discovery.reverse()
		for item in discovery:
			url = str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try: 
					title = str(item.select('h3')[0].get_text())
					amount = str(item.select('.keypoint span')[0].get_text())
					img = 'http://www.wutongnews.com/static/media/images/usericon/u21803996393528117528fm26gp0.jpg' 
					price = '暂无'
					infor = '众测'
					count = str(item.select('.start_time.have_end_time')[0].get_text()).replace(' ','').replace('\n','')
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass
	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def discoverytaihuoniao(request):
	discoveryhost = Discoveryhost.objects.get(id = 20)
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = 'User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
	dcap["phantomjs.page.settings.loadImages"] = False
	driver = webdriver.PhantomJS(desired_capabilities=dcap)
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'https://www.taihuoniao.com/try'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.card')
		discovery.reverse()
		for item in discovery:
			url = str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try: 
					ifapply = str(item.select('.ribbon.apply')[0].get_text()).replace(' ','').replace('\n','')
					title = str(item.select('h2 a')[0].attrs['title'])
					amount = str(item.select('.column')[0].get_text())
					img = str(item.select('a')[0].attrs['data-original'])
					price = ''
					infor = '免费试用'
					count = '申请中'
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass
	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def discoveryzhinengjie(request):
	discoveryhost = Discoveryhost.objects.get(id = 12)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://www.znjchina.com/e/action/ListInfo.php?classid=16&syzt=%E7%94%B3%E8%AF%B7%E4%B8%AD&ph=1&on=2'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.applyfor')
		discovery.reverse()
		for item in discovery:
			url = str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try: 
					title = str(item.select('.title')[0].get_text())
					amount = str(item.select('.info tr td')[0].get_text())
					img = str(item.select('a img')[0].attrs['src'])
					price = '暂无价格'
					infor = '免费试用'
					count = str(item.select('.countdown')[0].get_text()).replace(' ','').replace('\n','')
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass
	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')



def discoverywaishetianxia(request):
	discoveryhost = Discoveryhost.objects.get(id = 13)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'https://www.wstx.com/pubtest/list/1'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.list_test li')
		discovery.reverse()
		for item in discovery:
			url = 'https://www.wstx.com' + str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try: 
					title = str(item.select('a')[0].attrs['title'])
					amount = str(item.select('.keypoint span')[0].get_text())
					img = 'http://5b0988e595225.cdn.sohucs.com/images/20170724/a11aa00a9e35442d98a1fa0f8d194b05.jpeg'
					price = '暂无价格'
					infor = '免费试用'
					count = '申请中'
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass
	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')



def discoverygaoji(request):
	discoveryhost = Discoveryhost.objects.get(id = 2)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://tryout.igao7.com/default/index/status/3'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.applyfor')
		discovery.reverse()
		for item in discovery:
			url = str(item.select('.pic a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try: 
					title = str(item.select('.exam-con a')[0].get_text())
					amount = str(item.select('.exam-con .con-num.clr .goods')[0].get_text())
					img = str(item.select('.pic a img')[0].attrs['data-original'])
					price = '暂无价格'
					infor = '免费试用'
					count = ''
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass
	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')



def discoveryzol(request):
	discoveryhost = Discoveryhost.objects.get(id = 15)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://try.zol.com.cn/activity/'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.item')
		discovery.reverse()
		for item in discovery:
			url = 'http://try.zol.com.cn/' + str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try:
					if str(item.select('.ico.ico-apply')[0].get_text()) == '报名':
						title = str(item.select('h3')[0].get_text())
						amount = str(item.select('.item-intro li')[2].get_text())
						img = str(item.select('a img')[0].attrs['src'])
						price = str(item.select('.item-intro li')[0].get_text())
						infor = '免费试用'
						count = str(item.select('.timebox')[0].get_text())
						newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
						newdiscovery.save()
					else:
						pass
				except:
					pass
	except:
		pass

	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def discoveryzhiyou(request):
	discoveryhost = Discoveryhost.objects.get(id = 14)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://pingce.zhiyoo.com/pstatus_2.html'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.image_product')
		discovery.reverse()
		for item in discovery:
			url = 'http://pingce.zhiyoo.com/' + str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try:
					title = str(item.select('.subject')[0].get_text())
					amount = str(item.select('.test_info span')[0].get_text())
					img = str(item.select('.pic img')[0].attrs['data-original'])
					price = '暂无价格'
					infor = '免费试用'
					count = str(item.select('.stime .start_time.have_end_time')[0].get_text()).replace(' ','').replace('\n','')
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass

	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def discoverymogu(request):
	discoveryhost = Discoveryhost.objects.get(id = 3)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://www.yzmg.com/event/index.php?act=open'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.item-sy')
		discovery.reverse()
		for item in discovery:
			url = 'http://www.yzmg.com' + str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try:
					title = str(item.select('.title')[0].get_text())
					amount = '数量：' + str(item.select('.num.cell')[0].get_text()).replace(' ','').replace('\n','')
					img = str(item.select('img')[0].attrs['src'])
					price = '暂无价格'
					infor = '免费试用'
					count = str(item.select('.item-sy-status')[0].get_text())
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass

	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')






def discoverygaoqing(request):
	discoveryhost = Discoveryhost.objects.get(id = 5)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://www.hdpfans.com/plugin.php?id=tryout&ac=article&status=1'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.article2')
		discovery.reverse()
		for item in discovery:
			url = 'http://www.hdpfans.com/' + str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try: 
					title = str(item.select('.info a')[0].get_text())
					amount = str(item.select('.sidk_wd')[0].get_text()).replace(' ','').replace('\n','')
					img = 'http://www.hdpfans.com/' + str(item.select('a img')[0].attrs['src'])
					price = str(item.select('.sidk_wd')[2].get_text()).replace(' ','').replace('\n','')
					infor = '免费试用'
					count = str(item.select('.timestr span')[0].get_text())
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass

	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def discoveryznds(request):
	discoveryhost = Discoveryhost.objects.get(id = 6)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://www.znds.com/ce-plist-1-1.html'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.ul-list .left')
		discovery.reverse()
		for item in discovery:
			url = str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try:
					title = str(item.select('.item-title')[0].attrs['title'])
					amount = '数量：' + str(item.select('.qty')[0].get_text())
					img = str(item.select('a img')[0].attrs['src'])
					price = str(item.select('.price')[0].get_text())
					infor = '免费试用'
					count = ''
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass

	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def discoveryit168(request):
	discoveryhost = Discoveryhost.objects.get(id = 7)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://shike.it168.com/activities-1.html'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('#cont li')
		discovery.reverse()
		for item in discovery:
			url = 'http://shike.it168.com' + str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try:
					title = str(item.select('p a')[0].get_text())
					amount = str(item.select('.shuliang .n1')[0].get_text())
					img = str(item.select('a img')[0].attrs['src'])
					price = '暂无价格'
					infor = '免费试用'
					count = str(item.select('.time5')[0].get_text())
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass		
	except:
		pass

	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')



def discoveryjingdong(request):
	discoveryhost = Discoveryhost.objects.get(id = 8)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'https://pingce.jd.com/index.html?from=header'
	try:
		driver.get(urlpage)
		time.sleep(2)
		driver.find_element_by_id("check_more_loader").click()
		time.sleep(2)
		driver.find_element_by_id("check_more_loader").click()
		time.sleep(2)
		driver.find_element_by_id("check_more_loader").click()
		time.sleep(2)
		driver.find_element_by_id("check_more_loader").click()
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.projectChild')
		discovery.reverse()
		for item in discovery:
			url = 'https://pingce.jd.com' + str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
				pass
			except:
				try:
					str(item.select('.color02.font-s.font16')[-1].get_text())
					if str(item.select('.color02.font-s.font16')[-1].get_text()) == '申请中':
						amount = str(item.select('.text-c')[1].get_text()).replace(' ','').replace('\n','')
						img = 'https:' + str(item.select('a img')[0].attrs['src'])
						title = str(item.select('.fl')[0].get_text())
						price = str(item.select('.text-c')[2].get_text()).replace(' ','').replace('\n','')
						infor = '免费试用'
						count = '距申请结束还有：' + str(item.select('#day_show')[0].get_text())
						newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
						newdiscovery.save()
					else:
						pass
				except:
					pass
	except:
		pass

	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')






def discoveryzhinengbang(request):
	discoveryhost = Discoveryhost.objects.get(id = 9)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'https://www.iznb.cn/activity'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.at-item.middle-state')
		discovery.reverse()
		for item in discovery:
			url = 'https://www.iznb.cn' + str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
				pass
			except:
				title = str(item.select('.at-product-name')[0].get_text())
				amount = str(item.select('.clearfix li')[0].get_text())
				img = 'https:' + str(item.select('.at-pic img')[0].attrs['src'])
				price = '暂无价格'
				infor = '免费试用'
				count = str(item.select('.float-info')[0].get_text())
				newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
				newdiscovery.save()
	except:
		pass

	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def discoverytaipingyang(request):
	discoveryhost = Discoveryhost.objects.get(id = 10)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://try.pconline.com.cn/'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.art')
		discovery.reverse()
		for item in discovery:
			url = str(item.select('.img-area')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try:
					item.select('.applying')[0].get_text()
					title = str(item.select('.art-tit a')[0].get_text())
					amount = str(item.select('.approve-num')[0].get_text())
					price = '暂无价格'
					infor = '免费试用'
					count = str(item.select('.JcountTimer')[0].get_text())
					img = 'http://www.wutongnews.com/static/media/images/usericon/timg.jpg'
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass		
	except:
		pass

	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def discoveryyewan(request):
	discoveryhost = Discoveryhost.objects.get(id = 11)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://www.yeoner.com/zhongce'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.layout_li')
		discovery.reverse()
		for item in discovery:
			url = str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try:
					item.select('.test_apply')[0].get_text()
					title = str(item.select('a h3')[0].get_text())
					amount = str(item.select('.test_count span')[1].get_text())
					price = str(item.select('.test_count span')[0].get_text())
					infor = '免费试用'
					count = str(item.select('.test_state span')[0].get_text())
					img = str(item.select('a img')[0].attrs['src'])
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass		
	except:
		pass

	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def updatediscoveryyewan(request):
	discovery = Discovery.objects.all().filter(host = 11).order_by('-id')[0:8]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.user-login.apply_now.btn')[0].get_text()).replace(' ','').replace('\n','') == '立即申请':
					count = '剩余时间：' + str(soup.select('.endtime')[0].get_text())
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			item.count = count
			item.save(update_fields=['count'])
		except:
			pass
	driver.close()
	yewan = Discoveryhost.objects.get(id = 11)
	yewan.save()	
	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def updatediscoveryzhinengbang(request):
	discovery = Discovery.objects.all().filter(host = 9).order_by('-id')[0:8]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")

			try:
				if str(soup.select('.ac-apply-btn.need-login')[0].get_text()) == '我要申请':
					count = str(soup.select('.apply-count-down span')[0].get_text())
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			price = '￥' + str(soup.select('.ac-info-l.fl p')[1].get_text())

			item.count = count
			item.price = price
			item.save()
		except:
			pass
	driver.close()
	zhinengbang = Discoveryhost.objects.get(id = 9)
	zhinengbang.save()	
	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')





def updatediscoverytengxuncar(request):
	discovery = Discovery.objects.all().filter(host = 18).order_by('-id')[0:10]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.u-btn.u-yellow')[0].get_text()).replace(' ','').replace('\n','') == '免费申请':
					count = '申请中'
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			item.count = count
			item.save(update_fields=['count'])
		except:
			pass
	driver.close()
	tengxuncar = Discoveryhost.objects.get(id = 18)
	tengxuncar.save()	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def updatediscoveryjuyoufan(request):
	discoveryhost = Discoveryhost.objects.get(id = 17)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://try.pchouse.com.cn/'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.pic-txt.pic-txtb')
		discovery.reverse()
		for item in discovery:
			url = str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
				try:
					btn = str(item.select('.btn.btn-1')[0].get_text())
					discovery.count = str(item.select('.count-down.count-downa')[0].get_text())
					discovery.save(update_fields=['count'])
				except:
					discovery.count = '申请结束'
					discovery.save(update_fields=['count'])
			except:
				pass
	except:
		pass
	driver.close()
	discoveryhost.save()	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')






def updatediscoveryairanshao(request):
	discovery = Discovery.objects.all().filter(host = 16).order_by('-id')[0:10]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.status-link.btn.js-modal-login')[0].get_text()).replace(' ','').replace('\n','') == '立即申请':
					count = str(soup.select('.status-time')[0].get_text()).replace(' ','').replace('\n','')
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			item.count = count
			item.save(update_fields=['count'])
		except:
			pass
	driver.close()
	airanshao = Discoveryhost.objects.get(id = 16)
	airanshao.save()	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def updatediscoverywaishetianxia(request):
	discoveryhost = Discoveryhost.objects.get(id = 13)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'https://www.wstx.com/pubtest/list/2'
	try:
		driver.get(urlpage)
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.list_test li')
		discovery.reverse()
		for item in discovery:
			url = 'https://www.wstx.com' + str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
				discovery.count = '申请结束'
				discovery.save(update_fields=['count'])
			except:
				pass
	except:
		pass
	driver.close()
	discoveryhost.save()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')






def updatediscoveryzhinengjie(request):
	discovery = Discovery.objects.all().filter(host = 12).order_by('-id')[0:8]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(5)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('#divdown1')[0].get_text()) == '已过期':
					count = '申请结束'
				else:
					count = str(soup.select('#divdown1')[0].get_text())
			except:
				count = '申请结束'
			item.count = count
			item.price = str(soup.select('.big.cohf')[0].get_text())
			item.save()
		except:
			pass
	driver.close()
	zhinengjie = Discoveryhost.objects.get(id = 12)
	zhinengjie.save()	
	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')



def updatediscoverytaipingyang(request):
	discovery = Discovery.objects.all().filter(host = 10).order_by('-id')[0:5]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.act-btn.btn')[0].get_text()) == '我要申请':
					count = str(soup.select('.JcountTimer')[0].get_text())
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			item.count = count
			item.save(update_fields=['count'])
		except:
			pass
	driver.close()
	taipingyang = Discoveryhost.objects.get(id = 10)
	taipingyang.save()	
	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def discoverysina(request):
	discoveryhost = Discoveryhost.objects.get(id = 4)
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	urlpage = 'http://zhongce.sina.com.cn/activity/lists'
	try:
		driver.get(urlpage)
		time.sleep(2)
		driver.find_element_by_xpath('//a[@datanum="1"]').click();
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		discovery = soup.select('.zcCard')
		discovery.reverse()
		for item in discovery:
			url = str(item.select('a')[0].attrs['href'])
			try:
				discovery = Discovery.objects.get(addr = url)
			except:
				try:
					title = str(item.select('.detail .title')[0].get_text()).replace(' ','').replace('\n','')
					amount = str(item.select('.num.clearfix .fen')[0].get_text())
					img = str(item.select('a img')[0].attrs['src'])
					price = str(item.select('.num.clearfix .price')[0].get_text())
					infor = '免费试用'
					count = ''
					newdiscovery = Discovery(host = discoveryhost, img = img, title = title, count = count, addr = url, price = price, infor = infor, amount = amount)
					newdiscovery.save()
				except:
					pass
	except:
		pass
	driver.close()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def updatediscoveryjingdong(request):
	discovery = Discovery.objects.all().filter(host = 8).order_by('-id')[0:10]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.project-btns span')[1].get_text()) == '申请评测':
					count = str(soup.select('#CountMsg')[0].get_text())
				else:
					count = '申请结束'
			except:
				count = '申请结束'

			item.count = count
			item.save(update_fields=['count'])
		except:
			pass
	driver.close()
	jingdong = Discoveryhost.objects.get(id = 8)
	jingdong.save()	
	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def updatediscoveryit168(request):
	discovery = Discovery.objects.all().filter(host = 7).order_by('-id')[0:8]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.daojishi2 a')[0].get_text()) == '我要参加':
					count = str(soup.select('.daojishi2 p')[0].get_text())
				else:
					count = '申请结束'
			except:
				count = '申请结束'

			item.count = count
			item.save(update_fields=['count'])
		except:
			pass
	driver.close()
	it168 = Discoveryhost.objects.get(id = 7)
	it168.save()	
	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')



def updatediscoveryznds(request):
	discovery = Discovery.objects.all().filter(host = 6).order_by('-id')[0:15]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.apply-button.banner-button.button.btn.left')[0].get_text()) == '立即申请':
					count = str(soup.select('.banner-time')[0].get_text()).replace(' ','').replace('\n','')
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			item.count = count
			item.save(update_fields=['count'])
		except:
			pass
	driver.close()
	znds = Discoveryhost.objects.get(id = 6)
	znds.save()	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def updatediscoverysmzdm(request):
	discovery = Discovery.objects.all().filter(host = 19).order_by('-id')[0:15]
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = 'User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
	dcap["phantomjs.page.settings.loadImages"] = False
	driver = webdriver.PhantomJS(desired_capabilities=dcap)
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.banner_btn a')[0].get_text()) == '立即申请':
					count = '申请中'
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			item.price = str(soup.select('.provider_box .lFloat p')[1].get_text())
			item.count = count
			item.save()
		except:
			pass
	driver.close()
	smzdm = Discoveryhost.objects.get(id = 19)
	smzdm.save()	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def updatediscoverytaihuoniao(request):
	discovery = Discovery.objects.all().filter(host = 20).order_by('-id')[0:10]
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = 'User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
	dcap["phantomjs.page.settings.loadImages"] = False
	driver = webdriver.PhantomJS(desired_capabilities=dcap)
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.ui.white.applytry.inverted.button')[0].get_text()).replace(' ','').replace('\n','') == '申请试用':
					count = '剩余时间：' + str(soup.select('.ui.divided.horizontal.timer.list')[0].get_text())
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			item.price = str(soup.select('.user.action')[0].get_text()).replace(' ','').replace('\n','')
			item.count = count
			item.save()
		except:
			pass
	driver.close()
	taihuoniao = Discoveryhost.objects.get(id = 20)
	taihuoniao.save()	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')



def updatediscoverygaoqing(request):
	discovery = Discovery.objects.all().filter(host = 5).order_by('-id')[0:15]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.alubtn.btn_1')[0].get_text()) == '立即申请':
					count = str(soup.select('.countdown .xi1')[0].get_text())
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			item.count = count
			item.save(update_fields=['count'])
		except:
			pass
	driver.close()
	gaoqing = Discoveryhost.objects.get(id = 5)
	gaoqing.save()	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')





def updatediscoverygaoji(request):
	discovery = Discovery.objects.all().filter(host = 2).order_by('-id')[0:15]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.btn.applyfor')[0].get_text()).replace(' ','').replace('\n','') == '立即申请':
					count = str(soup.select('.countdown')[0].get_text())
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			price = str(soup.select('.m-l p')[1].get_text())
			item.count = count
			item.price = price
			item.save()
		except:
			pass
	driver.close()
	gaoji = Discoveryhost.objects.get(id = 2)
	gaoji.save()	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def updatediscoveryjiguo(request):
	discovery = Discovery.objects.all().filter(host = 1).order_by('-id')[0:30]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.card-link a')[0].get_text()) == "立即申请":
					count = str(soup.select('.event-banner-get-time')[0].get_text())
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			if item.infor == '折扣试用':
				try:
					amount = str(soup.select('.circle-box')[0].get_text()).replace(' ','').replace('\n','')
					item.amount = item.amount.split('+')[0] + '+' + amount
				except:
					pass
			else:
				pass
			item.count = count
			item.save()
		except:
			pass
	driver.close()
	jiguo = Discoveryhost.objects.get(id = 1)
	jiguo.save()
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')



def updatediscoveryzol(request):
	discovery = Discovery.objects.all().filter(host = 15).order_by('-id')[0:5]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			print 'test1'
			try:
				str(soup.select('.btn.ico-apply')[0].get_text())
				count = str(soup.select('.timebox')[0].get_text())
			except:
				count = '申请结束'
			item.count = count
			item.save(update_fields=['count'])
		except:
			pass
	driver.close()
	zol = Discoveryhost.objects.get(id = 15)
	zol.save()	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')



def updatediscoveryzhiyou(request):
	discovery = Discovery.objects.all().filter(host = 14).order_by('-id')[0:20]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.btns.clear .btn_red.fl')[0].get_text()) == '立即申请':
					count = str(soup.select('.start_time.have_end_time')[0].get_text()).replace(' ','').replace('\n','')
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			item.count = count
			item.save(update_fields=['count'])
		except:
			pass
	driver.close()
	zhiyou = Discoveryhost.objects.get(id = 14)
	zhiyou.save()	
	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')





def updatediscoverymogu(request):
	discovery = Discovery.objects.all().filter(host = 3).order_by('-id')[0:20]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr
			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.desc .btn a')[0].get_text()) == '免费申请':
					count = str(soup.select('.time')[0].get_text())
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			price = str(soup.select('.label em')[1].get_text())
			item.price = price
			item.count = count
			item.save()
		except:
			pass
	driver.close()
	mogu = Discoveryhost.objects.get(id = 3)
	mogu.save()	
	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')




def updatediscoverysina(request):
	discovery = Discovery.objects.all().filter(host = 4).order_by('-id')[0:5]
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	for item in discovery:
		try:
			url = item.addr

			driver.get(url)
			time.sleep(2)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
			try:
				if str(soup.select('.faceBtn')[0].get_text()) == '免费申请':
					count = str(soup.select('#faceTime')[0].get_text())
				else:
					count = '申请结束'
			except:
				count = '申请结束'
			item.count = count
			item.save(update_fields=['count'])
		except:
			pass
	driver.close()
	sina = Discoveryhost.objects.get(id = 4)
	sina.save()	
	data = {
		"ok": "over",
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')



def discoverystrart(request):
	ifcontinue = True
	while (ifcontinue):
		url1 = 'http://www.wutongnews.com/discovery/discoverysina/'
		url2 = 'http://www.wutongnews.com/discovery/updatediscoverysina/'
		url3 = 'http://www.wutongnews.com/discovery/discoverymogu/'
		url4 = 'http://www.wutongnews.com/discovery/updatediscoverymogu/'
		url5 = 'http://www.wutongnews.com/discovery/discoverygaoji/'
		url6 = 'http://www.wutongnews.com/discovery/updatediscoverygaoji/'
		url7 = 'http://www.wutongnews.com/discovery/discoveryjiguo/'
		url8 = 'http://www.wutongnews.com/discovery/updatediscoveryjiguo/'


		url9 = 'http://www.wutongnews.com/discovery/discoverygaoqing/'
		url10 = 'http://www.wutongnews.com/discovery/updatediscoverygaoqing/'
		url11 = 'http://www.wutongnews.com/discovery/discoveryznds/'
		url12 = 'http://www.wutongnews.com/discovery/updatediscoveryznds/'
		url13 = 'http://www.wutongnews.com/discovery/discoveryit168/'
		url14 = 'http://www.wutongnews.com/discovery/updatediscoveryit168/'
		url15 = 'http://www.wutongnews.com/discovery/discoveryjingdong/'
		url16 = 'http://www.wutongnews.com/discovery/updatediscoveryjingdong/'
		url17 = 'http://www.wutongnews.com/discovery/discoveryzhinengbang/'
		url18 = 'http://www.wutongnews.com/discovery/updatediscoveryzhinengbang/'
		url19 = 'http://www.wutongnews.com/discovery/discoverytaipingyang/'
		url20 = 'http://www.wutongnews.com/discovery/updatediscoverytaipingyang/'
		url21 = 'http://www.wutongnews.com/discovery/discoveryyewan/'
		url22 = 'http://www.wutongnews.com/discovery/updatediscoveryyewan/'

		url23 = 'http://www.wutongnews.com/discovery/discoveryzhinengjie/'
		url24 = 'http://www.wutongnews.com/discovery/updatediscoveryzhinengjie/'
		url25 = 'http://www.wutongnews.com/discovery/discoverywaishetianxia/'
		url26 = 'http://www.wutongnews.com/discovery/updatediscoverywaishetianxia/'

		url27 = 'http://www.wutongnews.com/discovery/discoveryzhiyou/'
		url28 = 'http://www.wutongnews.com/discovery/updatediscoveryzhiyou/'
		url29 = 'http://www.wutongnews.com/discovery/discoveryzol/'
		url30 = 'http://www.wutongnews.com/discovery/updatediscoveryzol/'

		url31 = 'http://www.wutongnews.com/discovery/discoveryairanshao/'
		url32 = 'http://www.wutongnews.com/discovery/updatediscoveryairanshao/'
		url33 = 'http://www.wutongnews.com/discovery/discoveryjuyoufan/'
		url34 = 'http://www.wutongnews.com/discovery/updatediscoveryjuyoufan/'
		url35 = 'http://www.wutongnews.com/discovery/discoverytengxuncar/'
		url36 = 'http://www.wutongnews.com/discovery/updatediscoverytengxuncar/'

		url37 = 'http://www.wutongnews.com/discovery/discoverysmzdm/'
		url38 = 'http://www.wutongnews.com/discovery/updatediscoverysmzdm/'

		url39 = 'http://www.wutongnews.com/discovery/discoverytaihuoniao/'
		url40 = 'http://www.wutongnews.com/discovery/updatediscoverytaihuoniao/'


		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url1)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url2)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url3)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url4)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url5)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url6)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url9)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url10)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url11)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url12)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url13)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url14)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url15)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url16)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url17)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url18)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url19)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url20)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url21)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url22)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url23)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url24)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url25)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass


		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url26)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass


		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url27)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url28)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url29)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url30)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass



		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url31)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass


		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url32)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url33)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url34)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass


		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url35)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass


		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url36)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			dcap = dict(DesiredCapabilities.PHANTOMJS)
			dcap["phantomjs.page.settings.loadImages"] = False
			driver = webdriver.PhantomJS(desired_capabilities=dcap)
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url37)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass


		try:
			dcap = dict(DesiredCapabilities.PHANTOMJS)
			dcap["phantomjs.page.settings.loadImages"] = False
			driver = webdriver.PhantomJS(desired_capabilities=dcap)
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url38)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass


		try:
			dcap = dict(DesiredCapabilities.PHANTOMJS)
			dcap["phantomjs.page.settings.loadImages"] = False
			driver = webdriver.PhantomJS(desired_capabilities=dcap)
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url39)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass


		try:
			dcap = dict(DesiredCapabilities.PHANTOMJS)
			dcap["phantomjs.page.settings.loadImages"] = False
			driver = webdriver.PhantomJS(desired_capabilities=dcap)
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url40)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass


		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url7)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		try:
			driver = webdriver.PhantomJS()
			driver.set_page_load_timeout(30)  
			driver.set_script_timeout(30)
			driver.get(url8)
			time.sleep(60)
			driver.close()
			time.sleep(10)
		except:
			pass

		time.sleep(1800)


