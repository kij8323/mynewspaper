#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
import urllib2
import random
import string
import json
from django.http import HttpResponse
import hashlib
import rsa
import base64
import time
from urllib import quote, unquote
import urllib2
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Finance
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from products.models import Products
from accounts.models import MyUser
# import re, sys
# reload(sys)
# sys.setdefaultencoding( "utf-8" )
# Create your views here.

def weixinfinance(request):
	url = "www.baidu.com"
	key = "192006250b4c09247ec02edce69f6a2d"

	appid = 'appid' #微信支付分配的公众账号ID（企业号corpid即为此appId）
	mch_id = 'mch_id' #微信支付分配的商户号
	nonce_str = ''.join(random.sample(string.ascii_letters  +  string.digits, 32))  #随机字符串，长度要求在32位以内
	# sign = 'sign' #通过签名算法计算得出的签名值
	body = '押金质押' #商品简单描述，该字段请按照规范传递
	out_trade_no = '1' #商户系统内部订单号，要求32个字符内，只能是数字、大小写字母_-|*@ ，且在同一个商户号下唯一
	total_fee = 100.88 #订单总金额，单位为分
	spbill_create_ip = "10.10.10.10 " #APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
	notify_url =  "www.baidu.com" #异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数
	trade_type = 'trade_type' #取值如下：JSAPI，NATIVE，APP等
	product_id = 'product_id' #trade_type=NATIVE时（即扫码支付），此参数必传。此参数为二维码中包含的商品ID，商户自行定义。



	stringA = "appid="  +  appid  +  "&"\
	 + "body=" + body + "&"\
	 + "mch_id=" + mch_id + "&"\
	 + "nonce_str=" + nonce_str + "&"\
	 + "notify_url=" + notify_url + "&"\
	 + "out_trade_no=" + out_trade_no + "&"\
	 + "product_id=" + product_id + "&"\
	 + "spbill_create_ip=" + spbill_create_ip + "&"\
	 + "total_fee=" + str(total_fee) + "&"\
	 + "trade_type=" + trade_type + "&"\
	 + "key=" + key


	stringSignTemp = hashlib.md5()
	stringSignTemp.update(stringA)
	sign = stringSignTemp.hexdigest().upper()


	xmlvalues = "<appid>"  +  appid  +  "</appid>"\
	 + "<mch_id>" + mch_id + "</mch_id>"\
	 + "<nonce_str>" + nonce_str + "</nonce_str>"\
	 + "<body>" + body + "</body>"\
	 + "<out_trade_no>" + out_trade_no + "</out_trade_no>"\
	 + "<total_fee>" + str(total_fee) + "</total_fee>"\
	 + "<spbill_create_ip>" + spbill_create_ip + "</spbill_create_ip>"\
	 + "<notify_url>" + notify_url + "</notify_url>"\
	 + "<trade_type>" + trade_type + "</trade_type>"\
	 + "<product_id>" + product_id + "</product_id>"\
	 + "<sign>" + sign + "</sign>"


	# req = urllib2.Request(url = url, headers = {'Content-Type' : 'text/xml'}, data=xmlvalues)
	# response = urllib2.urlopen(req)
	# res = response.read()

	data = {
		"xmlvalues":xmlvalues,
		"stringA":stringA,
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


@login_required(login_url='/user/loggin/')
def alipayfinance(request):
	one = request.POST.get('one')
	productsid = request.POST.get('products')
	if int(one)>0 and productsid:
		products = Products.objects.get(id = int(productsid))

		if len(productsid) == 1:
			productsid = "000"+productsid
		elif len(productsid) == 2:
			productsid = "00"+productsid
		elif len(productsid) == 3:
			productsid = "0"+productsid
		elif len(productsid) == 4:
			pass
		elif len(productsid) > 4:
			return HttpResponseRedirect("http://www.wutongnews.com")

		listb = str(products.one+1)
		listl = str(products.one+int(one))

		if len(listb) == 1:
			listb = "00000"+listb
		elif len(listb) == 2:
			listb = "0000"+listb
		elif len(listb) == 3:
			listb = "000"+listb
		elif len(listb) == 4:
			listb = "00"+listb
		elif len(listb) == 5:
			listb = "0"+listb
		elif len(listb) == 6:
			pass
		elif len(listb) > 6:
			return HttpResponseRedirect("http://www.wutongnews.com")


		if len(listl) == 1:
			listl = "00000"+listl
		elif len(listl) == 2:
			listl = "0000"+listl
		elif len(listl) == 3:
			listl = "000"+listl
		elif len(listl) == 4:
			listl = "00"+listl
		elif len(listl) == 5:
			listl = "0"+listl
		elif len(listl) == 6:
			pass
		elif len(listl) > 6:
			return HttpResponseRedirect("http://www.wutongnews.com")

		userlist = productsid + "_" + str(time.time()) + "_" + listb + "-" + listl
	else:
		return HttpResponseRedirect("http://www.wutongnews.com")
	url = "https://openapi.alipay.com/gateway.do"

	app_id = "2017052407326498"
	method = "alipay.trade.page.pay"
	charset = "utf-8"
	sign_type = "RSA2"
	timestamp = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
	version = "1.0"
	out_trade_no = str(userlist)
	product_code = "FAST_INSTANT_TRADE_PAY"
	total_amount = int(one)
	subject = str(productsid)
	biz_content = str({"out_trade_no":out_trade_no,"product_code":product_code,"subject":subject,"total_amount":total_amount})
	notify_url = "http://www.wutongnews.com/alipay/notify/finance/"

	stringA = "app_id="  +  app_id  +  "&"\
	 + "biz_content=" + biz_content + "&"\
	 + "charset=" + charset + "&"\
	 + "method=" + method + "&"\
	 + "notify_url=" + notify_url + "&"\
	 + "sign_type=" + sign_type + "&"\
	 + "timestamp=" + timestamp + "&"\
	 + "version=" + version

	# stringA = stringA.replace(' ','%20')
	# print stringA
	with open('/home/shen/Documents/paperproject/mynewspaper/finance/privkey.txt','r') as f:
	    privkey = rsa.PrivateKey.load_pkcs1(f.read())

	signature = rsa.sign(stringA, privkey, 'SHA-256')
	signature = base64.b64encode(signature)
	sign = signature

	stringB = "app_id=" + quote(app_id) + "&"\
	 + "biz_content=" + quote(biz_content) + "&"\
	 + "charset=" + quote(charset) + "&"\
	 + "method=" + quote(method) + "&"\
	 + "notify_url=" + quote(notify_url) + "&"\
	 + "sign_type=" + quote(sign_type) + "&"\
	 + "timestamp=" + quote(timestamp) + "&"\
	 + "version=" + quote(version) + "&"\
	 + "sign=" + quote(sign)

	requesturl = url + "?" + stringB

	try:
		finance = Finance.objects.get(out_trade_no = out_trade_no)
	except:
		finance = Finance(user = request.user, out_trade_no = out_trade_no, total_amount = total_amount, products = products)
		finance.save()

	return HttpResponseRedirect(requesturl)

@csrf_exempt
def alipaynotifyfinance(request):
	notify_dict = {}
	if request.POST.get('notify_time'):
		notify_dict['notify_time'] = request.POST.get('notify_time')
	if request.POST.get('notify_type'):
		notify_dict['notify_type'] = request.POST.get('notify_type')
	if request.POST.get('notify_id'):
		notify_dict['notify_id'] = request.POST.get('notify_id')
	if request.POST.get('charset'):
		notify_dict['charset'] = request.POST.get('charset')
	if request.POST.get('version'):
		notify_dict['version'] = request.POST.get('version')
	if request.POST.get('auth_app_id'):
		notify_dict['auth_app_id'] = request.POST.get('auth_app_id')
	if request.POST.get('trade_no'):
		notify_dict['trade_no'] = request.POST.get('trade_no')
	if request.POST.get('app_id'):
		notify_dict['app_id'] = request.POST.get('app_id')
	if request.POST.get('out_trade_no'):
		notify_dict['out_trade_no'] = request.POST.get('out_trade_no')
	if request.POST.get('out_biz_no'):
		notify_dict['out_biz_no'] = request.POST.get('out_biz_no')
	if request.POST.get('buyer_id'):
		notify_dict['buyer_id'] = request.POST.get('buyer_id')
	if request.POST.get('seller_id'):
		notify_dict['seller_id'] = request.POST.get('seller_id')
	if request.POST.get('trade_status'):
		notify_dict['trade_status'] = request.POST.get('trade_status')
	if request.POST.get('total_amount'):
		notify_dict['total_amount'] = request.POST.get('total_amount')
	if request.POST.get('receipt_amount'):
		notify_dict['receipt_amount'] = request.POST.get('receipt_amount')
	if request.POST.get('invoice_amount'):
		notify_dict['invoice_amount'] = request.POST.get('invoice_amount')
	if request.POST.get('buyer_pay_amount'):
		notify_dict['buyer_pay_amount'] = request.POST.get('buyer_pay_amount')
	if request.POST.get('point_amount'):
		notify_dict['point_amount'] = request.POST.get('point_amount')
	if request.POST.get('refund_fee'):
		notify_dict['refund_fee'] = request.POST.get('refund_fee')
	if request.POST.get('subject'):
		notify_dict['subject'] = request.POST.get('subject')
	if request.POST.get('body'):
		notify_dict['body'] = request.POST.get('body')
	if request.POST.get('gmt_create'):
		notify_dict['gmt_create'] = request.POST.get('gmt_create')
	if request.POST.get('gmt_payment'):
		notify_dict['gmt_payment'] = request.POST.get('gmt_payment')
	if request.POST.get('gmt_refund'):
		notify_dict['gmt_refund'] = request.POST.get('gmt_refund')
	if request.POST.get('gmt_close'):
		notify_dict['gmt_close'] = request.POST.get('gmt_close')
	if request.POST.get('fund_bill_list'):
		notify_dict['fund_bill_list'] = request.POST.get('fund_bill_list')
	if request.POST.get('voucher_detail_list'):
		notify_dict['voucher_detail_list'] = request.POST.get('voucher_detail_list')
	if request.POST.get('passback_params'):
		notify_dict['passback_params'] = request.POST.get('passback_params')

	for item in notify_dict.keys():
		notify_dict[item] = unquote(notify_dict[item])
	
	notify_dict= sorted(notify_dict.items(), key=lambda d:d[0]) 

	notify_string = ''

	for item in notify_dict:
		notify_string = notify_string + str(item[0]) + '=' + str(item[1]) + "&"
	notify_string = notify_string[:-1]



	#sign = base64.b64decode(request.POST.get('sign'))
	sign = base64.b64decode(request.POST.get('sign'))
	with open('/home/shen/Documents/paperproject/mynewspaper/finance/pubkey.txt', 'r') as f:
		pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(f.read())

	try:
		verify = rsa.verify(notify_string, sign, pubkey)
		try:
			finance = Finance.objects.get(out_trade_no = unquote(str(request.POST.get('out_trade_no'))))
			if ("TRADE_SUCCESS" == unquote(str(request.POST.get('trade_status'))) and finance.trade_status == False) or ("TRADE_FINISHED" == unquote(str(request.POST.get('trade_status'))) and finance.trade_status == False):
				finance.trade_status = True
				finance.receipt_amount = unquote(str(request.POST.get('receipt_amount')))
				finance.buyer_id = unquote(str(request.POST.get('buyer_id')))
				finance.trade_no = unquote(str(request.POST.get('trade_no')))
				finance.out_biz_no = unquote(str(request.POST.get('out_biz_no')))
				finance.save()
				products = finance.products
				products.one = products.one + int(float(finance.receipt_amount))
				products.save(update_fields=['one'])
				return HttpResponse("success")
			else:
				return HttpResponse("failure") 
		except:
			return HttpResponse("failure") 
	except:
		return HttpResponse("failure") 


def alipayredirectfinance(request):
	data = {
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def alipaygatewayfinance(request):
	data = {
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def weixingatewayfinance(request):
	data = {
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def onebillpage(request, user_id):
	user = MyUser.objects.get(id = user_id)
	onebill = Finance.objects.filter(trade_status = True).filter(user = user).order_by('-id')
	context = {
		'onebill': onebill,
	}
	return render(request, 'onebillpage.html',  context)
