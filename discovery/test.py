#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib  
import urllib2  
from bs4 import BeautifulSoup
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   
import re
import time
# try:
# 	url = 'http://www.jiguo.com/event/index/1594.html'
# 	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
# 	headers = { 'User-Agent' : user_agent }  
# 	request = urllib2.Request(url, headers = headers)  
# 	response = urllib2.urlopen(request)  
# 	html = response.read()
# 	soup = BeautifulSoup(html, "lxml")

# 	try:
# 		print soup.select('.f3 .tag')[0].get_text()
# 		print soup.select('.event-banner-get-time')[0].get_text()
# 		print soup.select('.banner-img-box img')[0].attrs['src']
# 		print soup.select('.right-title')[0].get_text()
# 		print soup.select('.f2 .tag')[0].get_text()
# 	except:
# 		print str(soup.select('.circle-box .c3')[1].get_text())
# 		print soup.select('.event-banner-get-time')[0].get_text()
# 		print soup.select('.banner-img-box img')[0].attrs['src']
# 		print soup.select('.right-title')[0].get_text()
# 		print soup.select('.circle-box .c2')[0].get_text()



# except urllib2.URLError, e:
# 	if hasattr(e,"code"):
# 		print e.code
# 	if hasattr(e,"reason"):
# 		print e.reason


from selenium import webdriver


import traceback


 

try:
	driver = webdriver.PhantomJS()
	driver.set_page_load_timeout(30)  
	driver.set_script_timeout(30)
	driver.get("https://pingce.jd.com/index.html?from=header")
	# # time.sleep(2)
	# #driver.findElement(By.xpath("//button[@type='button']")).click();
	# time.sleep(2)
	# #x =  driver.find_element_by_xpath(By.XPATH, "//li//a[@data-type='open']").click();
	# driver.find_element_by_xpath('//a[@datanum="1"]').click();
	# time.sleep(2)
	# for item in x:
	# 	print item
	# # driver.find_element_by_xpath("//li[@data-type='open']").click()
	# # print  driver.find_element_by_xpath(//xpath("li[@data-type='open']"));
	# # time.sleep(2)
	# # driver.find_element_by_id("check_more_loader").click()
	driver.find_element_by_id("check_more_loader").click()
	time.sleep(2)
	driver.find_element_by_id("check_more_loader").click()
	time.sleep(2)
	driver.find_element_by_id("check_more_loader").click()
	time.sleep(2)
	driver.find_element_by_id("check_more_loader").click()
	time.sleep(2)
	html = driver.page_source
	driver.quit()
	soup = BeautifulSoup(html, "lxml")

	file_object = open('test.html', 'w')
	file_object.write(html)
	file_object.close( )

	# print str(soup.select('.ac-apply-btn.need-login')[0].get_text())
	# print str(soup.select('.apply-count-down span')[0].get_text())
	# print str(soup.select('.ac-info-l.fl p')[1].get_text())
	# print 'http://www.jiguo.com/' + str(soup.select('.event-class-list ul li a')[0].attrs['href'])
	# print str(soup.select('.event-class-list ul li a img')[0].attrs['src'])
	# print str(soup.select('.event-class-list ul li .e-title')[0].get_text())
	# print str(soup.select('.event-class-list ul li .e-query  span')[0].get_text())
	# print str(soup.select('.event-class-list ul li .e-item-hide-cell  .gray')[0].get_text())
	# print str(soup.select('.event-class-list ul li .e-item-hide-cell  .fr')[1].get_text())
	# soup.select('#change-type li a')[1]
	# print soup.select('#change-type li a')[1].click()

	# print str(soup.select('.ul-list .left a')[0].attrs['href'])
	# # print str(soup.select('#cont li a')[0].attrs['href'])
	# print 'http://shike.it168.com' + str(soup.select('#cont li a')[0].attrs['href'])
	# print str(soup.select('#cont li a img')[0].attrs['src'])
	# amount = len(soup.select('.projectChild'))
	# print amount
	# print 'https://pingce.jd.com' + str(soup.select('.projectChild a')[0].attrs['href'])
	# print 'https:' + str(soup.select('.projectChild a img')[0].attrs['src'])
	# print str(soup.select('.projectChild .fl')[0].get_text())
	# print str(soup.select('.projectChild .text-c')[1].get_text()).replace(' ','').replace('\n','')
	# print str(soup.select('.projectChild .text-c')[2].get_text()).replace(' ','').replace('\n','')
	# print str(soup.select('.projectChild .color02.font-s.font16')[-1].get_text())
	# print str(soup.select('.projectChild #day_show')[0].get_text())

	# print str(soup.select('.projectChild .color02.font-s.font16')[1].get_text())
	# print str(soup.select('.projectChild .color02.font-s.font16')[2].get_text())
	# pattern = re.compile(r'(\d+)')
	# res = re.findall(pattern, amount)
	# print res, res[0], res[1]
	# amount = str(soup.select('.chanpin_box2')[0].get_text())
	# pattern = re.compile(r'(\d+)')
	# res = re.findall(pattern, amount)
	# print res, res[0], res[1]
	# print str(soup.select('.daojishi2 p')[0].get_text())
	# print str(soup.select('#cont li .shuliang .n2')[0].get_text())
	# print str(soup.select('#cont li .time5')[0].get_text())
	# print str(soup.select('.ul-list .left .item-title')[0].attrs['title'])
	# print str(soup.select('.apply-button.banner-button.button.btn.left')[0].get_text())
	# print str(soup.select('.banner-time')[0].get_text()).replace(' ','').replace('\n','')
	# # print str(soup.select('.btn.applyfor')[0].get_text()).replace(' ','').replace('\n','')
	# # print str(soup.select('.applyfor .pic a img')[0].attrs['data-original'])
	# print str(soup.select('.m-l p')[1].get_text())
	# print str(soup.select('.applyfor .exam-con .con-num.clr .goods')[0].get_text())
	# print str(soup.select('.applyfor .exam-con .timestr')[0].get_text())
	# print str(soup.select('.art .art-tit a')[0].get_text())
	# print str(soup.select('.art .approve-num')[0].get_text())
	# print str(soup.select('.art .JcountTimer')[0].get_text())
	# print str(soup.select('.at-item.middle-state .clearfix li')[2].get_text())
	# print str(soup.select('.at-item.middle-state')[1].select('.clearfix li')[0].get_text())
	# print str(soup.select('.at-item.middle-state .at-tag')[0].get_text())
	# print str(soup.select('.img-area')[0].attrs['src'])
	# print str(soup.select('.act-btn.btn')[0].get_text())
	# print str(soup.select('.JcountTimer')[0].get_text())
	#print str(soup.select('.user-login.apply_now.btn')[0].get_text()).replace(' ','').replace('\n','')
	# print 'http://www.hdpfans.com/' + str(soup.select('.article2 a')[0].attrs['href'])
	# print 'http://www.hdpfans.com/' + str(soup.select('.article2 a img')[0].attrs['src'])
	# print str(soup.select('.article2 .ans.start')[0].get_text())
	# print str(soup.select('.article2 .info a')[0].get_text())
	# print str(soup.select('.article2 .sidk_wd')[0].get_text()).replace(' ','').replace('\n','')
	# print str(soup.select('.article2 .sidk_wd')[2].get_text()).replace(' ','').replace('\n','')
	# print str(soup.select('.article2 .timestr span')[0].get_text())
	# print 'http://www.yzmg.com' + str(soup.select('.item-sy a')[0].attrs['href'])
	# print str(soup.select('.item-sy img')[0].attrs['src'])
	# print str(soup.select('.item-sy .title')[0].get_text())
	# print '数量：' + str(soup.select('.item-sy .num.cell')[0].get_text()).replace(' ','').replace('\n','')
	# print str(soup.select('.item-sy .item-sy-status')[0].get_text()).replace(' ','').replace('\n','')


	
	# print str(soup.select('.layout_li .test_count span')[0].get_text())
	# print str(soup.select('.layout_li .test_count span')[1].get_text())
	# print str(soup.select('.layout_li a')[0].attrs['href'])
	# print str(soup.select('.layout_li a img')[0].attrs['src'])
	# print str(soup.select('.layout_li a h3')[0].get_text())
	# print str(soup.select('.layout_li .test_state span')[0].get_text())

	# print str(soup.select('.f3 .tag')[0].get_text())
	# [s.extract() for s in soup('span')] 
	# print str((soup.select('.text-c.hot_data .num')[1].get_text()))
	# print str((soup.select('.text-c.hot_data .num')[2].get_text()))
	# print str((soup.select('.project-title .fl')[0].get_text()))
	# print 'https:' + str((soup.select('.relative.pro_left_bg')[0].attrs['style'])).replace("background-image: url('",'').replace("');height:480px;width: 488px;",'')
	# pattern = re.compile('：.*?',re.S)
	# pattern = re.compile(r'(\d+)')
	# res = re.findall(pattern, amount)
	# print res, res[0], res[1]

	# # print soup.find_all(text=re.compile("申请"))
	# print 'http://shike.it168.com' + str(soup.select('.w1000_2 .l4 img')[0].attrs['src'])
	# # print str(soup.select('.banner-title')[0].get_text())
	# # print str(soup.select('.banner-left.left img')[0].attrs['src'])
	# # print str(soup.select('.daojishi2 p')[0].get_text())
	# # print str(soup.select('.daojishi2 a')[0].get_text())
	# print str(soup.select('#toApply'))
	# print str(soup.select('.project-btns span')[1].get_text())
	# if str(soup.select('.project-btns span')[1].get_text()) == '申请评测':
	# 	print str(soup.select('#day_show')[0].get_text())
	# else:
	# 	print ''
	# print str(soup.select('.countdown .xi1')[0].get_text())
	# print str(soup.select('.alubtn.btn_1')[0].get_text())
	# print str(soup.select('.faceImg img')[0].attrs['src'])
	# print str(soup.select('#faceRight h1')[0].get_text())
	# print str(soup.select('.faceDetail p em')[0].get_text())



except:
	traceback.print_exc()

