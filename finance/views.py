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
from accounts.models import MyUser, WeixinUser
from updatenew.models import Updatenew
import re, sys
# reload(sys)
# sys.setdefaultencoding( "utf-8" )
# Create your views here.
import qrcode
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP




@login_required(login_url='/user/loggin/')
def weixinfinancegz(request):
	state = request.GET.get('state')
	state = state.split('p')
	one = state[0]
	productsid = state[1]


	CODE = request.GET.get('code')
	url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=wxd7c459fd37fa1f3e&secret=88e9fb19bffe04b76178ef7ec4cf80cc&code="+CODE+"&grant_type=authorization_code"

	req = urllib2.Request(url)
	res_data = urllib2.urlopen(req)
	res = res_data.readline()
	openid = json.loads(res)['openid']


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
		userlist = userlist.replace('.', '')
	else:
		return HttpResponseRedirect("http://www.wutongnews.com")

	url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
	key = "192006250b4c09247ec02edce69f6a2d"
	spbill_create_ip = get_ip()

	appid = 'wxd7c459fd37fa1f3e' #微信支付分配的公众账号ID（企业号corpid即为此appId）
	mch_id = '1481008902' #微信支付分配的商户号
	nonce_str = ''.join(random.sample(string.ascii_letters  +  string.digits, 32))  #随机字符串，长度要求在32位以内

	# sign = 'sign' #通过签名算法计算得出的签名值
	body = "一元购" #商品简单描述，该字段请按照规范传递
	out_trade_no = str(userlist) #商户系统内部订单号，要求32个字符内，只能是数字、大小写字母_-|*@ ，且在同一个商户号下唯一
	total_fee = str(int(one)*100) #订单总金额，单位为分
	spbill_create_ip = spbill_create_ip #APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
	notify_url =  "http://www.wutongnews.com/weixin/notify/finance" #异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数
	trade_type = 'JSAPI' #取值如下：JSAPI，NATIVE，APP等
	product_id = str(products.id) #trade_type=NATIVE时（即扫码支付），此参数必传。此参数为二维码中包含的商品ID，商户自行定义。
	openid =str(openid)
	stringA = "appid="  +  appid  +  "&"\
	 + "body=" + body + "&"\
	 + "mch_id=" + mch_id + "&"\
	 + "nonce_str=" + nonce_str + "&"\
	 + "notify_url=" + notify_url + "&"\
	 + "openid=" + openid + "&"\
	 + "out_trade_no=" + out_trade_no + "&"\
	 + "product_id=" + product_id + "&"\
	 + "spbill_create_ip=" + spbill_create_ip + "&"\
	 + "total_fee=" + str(total_fee) + "&"\
	 + "trade_type=" + trade_type + "&"\
	 + "key=" + key

	stringSignTemp = hashlib.md5()
	stringSignTemp.update(stringA)
	sign = stringSignTemp.hexdigest().upper()

	xmlvalues = "<xml><appid>"  +  appid  +  "</appid>"\
	 + "<mch_id>" + mch_id + "</mch_id>"\
	 + "<nonce_str>" + nonce_str + "</nonce_str>"\
	 + "<body>" + body + "</body>"\
	 + "<openid>" + openid + "</openid>"\
	 + "<out_trade_no>" + out_trade_no + "</out_trade_no>"\
	 + "<total_fee>" + str(total_fee) + "</total_fee>"\
	 + "<spbill_create_ip>" + spbill_create_ip + "</spbill_create_ip>"\
	 + "<notify_url>" + notify_url + "</notify_url>"\
	 + "<trade_type>" + trade_type + "</trade_type>"\
	 + "<product_id>" + product_id + "</product_id>"\
	 + "<sign>" + sign + "</sign></xml>"

#	xmlvalues = xmlvalues.encode("UTF-8")  
	req = urllib2.Request(url = url, headers = {'Content-Type' : 'text/xml'}, data=xmlvalues)
	response = urllib2.urlopen(req)
	res = response.read()

	res = res.replace('[', '<');
	res = res.replace(']', '>');
	reprepay_id = ".*<prepay_id><!<CDATA<(.*)>>></prepay_id>.*"
	prepay_id = re.findall(reprepay_id, res)

	timeStamp = str(time.time()).replace('.', '')[0:10]
	signType = 'MD5'
	package = "prepay_id=" + prepay_id[0]

	stringB = "appId="  +  appid  +  "&"\
	 + "nonceStr=" + nonce_str + "&"\
	 + "package=" + package + "&"\
	 + "signType=" + signType + "&"\
	 + "timeStamp=" + timeStamp + "&"\
	 + "key=" + key


	stringSignTempgz = hashlib.md5()
	stringSignTempgz.update(stringB)
	paySign = stringSignTempgz.hexdigest().upper()



	try:
		finance = Finance.objects.get(out_trade_no = out_trade_no)
	except:
		finance = Finance(user = request.user, out_trade_no = out_trade_no, total_amount = str(one), products = products, start = int(listb), end = int(listl))
		finance.save()

	context = {

		"appid": appid,
		"nonce_str": nonce_str,
		"timestamp": timeStamp,
		'signtype': signType,
		'package': package,
		'paysign': paySign,
		}
	return render(request, 'weixinfinancegz.html',  context)




@login_required(login_url='/user/loggin/')
def weixinfinance(request):
	one = request.GET.get('one')
	productsid = request.GET.get('products')

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
		userlist = userlist.replace('.', '')
	else:
		return HttpResponseRedirect("http://www.wutongnews.com")

	url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
	key = "192006250b4c09247ec02edce69f6a2d"
	spbill_create_ip = get_ip()

	appid = 'wxd7c459fd37fa1f3e' #微信支付分配的公众账号ID（企业号corpid即为此appId）
	mch_id = '1481008902' #微信支付分配的商户号
	nonce_str = ''.join(random.sample(string.ascii_letters  +  string.digits, 32))  #随机字符串，长度要求在32位以内

	# sign = 'sign' #通过签名算法计算得出的签名值
	body = "一元购" #商品简单描述，该字段请按照规范传递
	out_trade_no = str(userlist) #商户系统内部订单号，要求32个字符内，只能是数字、大小写字母_-|*@ ，且在同一个商户号下唯一
	total_fee = str(int(one)*100) #订单总金额，单位为分
	spbill_create_ip = spbill_create_ip #APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
	notify_url =  "http://www.wutongnews.com/weixin/notify/finance" #异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数
	trade_type = 'NATIVE' #取值如下：JSAPI，NATIVE，APP等
	product_id = str(products.id) #trade_type=NATIVE时（即扫码支付），此参数必传。此参数为二维码中包含的商品ID，商户自行定义。

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

	xmlvalues = "<xml><appid>"  +  appid  +  "</appid>"\
	 + "<mch_id>" + mch_id + "</mch_id>"\
	 + "<nonce_str>" + nonce_str + "</nonce_str>"\
	 + "<body>" + body + "</body>"\
	 + "<out_trade_no>" + out_trade_no + "</out_trade_no>"\
	 + "<total_fee>" + str(total_fee) + "</total_fee>"\
	 + "<spbill_create_ip>" + spbill_create_ip + "</spbill_create_ip>"\
	 + "<notify_url>" + notify_url + "</notify_url>"\
	 + "<trade_type>" + trade_type + "</trade_type>"\
	 + "<product_id>" + product_id + "</product_id>"\
	 + "<sign>" + sign + "</sign></xml>"


	req = urllib2.Request(url = url, headers = {'Content-Type' : 'text/xml'}, data=xmlvalues)
	response = urllib2.urlopen(req)
	res = response.read()

	twocode =  res[-56:-21]
	img=qrcode.make(twocode)
	imgadd = "/home/shen/Documents/paperproject/static/media/images/qrcode/" + out_trade_no + ".png"
	img.save(imgadd)
	getimgadd = "images/qrcode/" + out_trade_no + ".png"
	try:
		finance = Finance.objects.get(out_trade_no = out_trade_no)
	except:
		finance = Finance(user = request.user, out_trade_no = out_trade_no, total_amount = str(one), products = products, qrcodeimage = getimgadd, start = int(listb), end = int(listl))
		finance.save()

	context = {
		"finance": finance,
		}
	return render(request, 'weixinfinance.html',  context)


@csrf_exempt
def weixinnotifyfinance(request):
	try:
		xml = request.read()
		xml = str(xml).encode('ascii','ignore')

		xml = xml.replace('[', '<');
		xml = xml.replace(']', '>');


		reappid = ".*<appid><!<CDATA<(.*)>>></appid>.*"
		rebank_type = ".*<bank_type><!<CDATA<(.*)>>></bank_type>.*"
		recash_fee = ".*<cash_fee><!<CDATA<(.*)>>></cash_fee>.*"
		refee_type = ".*<fee_type><!<CDATA<(.*)>>></fee_type>.*"
		reis_subscribe = ".*<is_subscribe><!<CDATA<(.*)>>></is_subscribe>.*"
		remch_id = ".*<mch_id><!<CDATA<(.*)>>></mch_id>.*"
		renonce_str = ".*<nonce_str><!<CDATA<(.*)>>></nonce_str>.*"
		reopenid = ".*<openid><!<CDATA<(.*)>>></openid>.*"
		reout_trade_no = ".*<out_trade_no><!<CDATA<(.*)>>></out_trade_no>.*"
		reresult_code = ".*<result_code><!<CDATA<(.*)>>></result_code>.*"
		rereturn_code = ".*<return_code><!<CDATA<(.*)>>></return_code>.*"
		resign = ".*<sign><!<CDATA<(.*)>>></sign>.*"
		retime_end = ".*<time_end><!<CDATA<(.*)>>></time_end>.*"
		retotal_fee = ".*<total_fee>(.*)</total_fee>.*"
		retrade_type = ".*<trade_type><!<CDATA<(.*)>>></trade_type>.*"
		retransaction_id = ".*<transaction_id><!<CDATA<(.*)>>></transaction_id>.*"

		appid = re.findall(reappid,xml)
		bank_type = re.findall(rebank_type,xml)
		cash_fee = re.findall(recash_fee,xml)
		fee_type = re.findall(refee_type,xml)
		is_subscribe = re.findall(reis_subscribe,xml)
		mch_id = re.findall(remch_id,xml)
		nonce_str = re.findall(renonce_str,xml)
		openid = re.findall(reopenid,xml)
		out_trade_no = re.findall(reout_trade_no,xml)
		result_code = re.findall(reresult_code,xml)
		return_code = re.findall(rereturn_code,xml)
		sign = re.findall(resign,xml)
		time_end = re.findall(retime_end,xml)
		total_fee = re.findall(retotal_fee,xml)
		trade_type = re.findall(retrade_type,xml)
		transaction_id = re.findall(retransaction_id,xml)

		xmlele = 'appid='+appid[0] + '&bank_type='+bank_type[0] + '&cash_fee='+cash_fee[0] + '&fee_type='+fee_type[0] + '&is_subscribe='+is_subscribe[0] + '&mch_id='+mch_id[0] + '&nonce_str='+nonce_str[0] + '&openid='+openid[0] + '&out_trade_no='+out_trade_no[0] + '&result_code='+result_code[0] + '&return_code='+return_code[0] + '&time_end='+time_end[0] + '&total_fee='+total_fee[0] + '&trade_type='+trade_type[0] + '&transaction_id='+transaction_id[0]
		
		sign = sign[0]
		out_trade_no = out_trade_no[0]
		total_fee = total_fee[0]
		return_code = return_code[0]

		xml = xmlele+"&key=192006250b4c09247ec02edce69f6a2d"


		stringSignTemp = hashlib.md5()
		stringSignTemp.update(xml)
		valisign = stringSignTemp.hexdigest().upper()



		if valisign == sign and return_code == "SUCCESS":
			try:
				finance = Finance.objects.get(out_trade_no = out_trade_no)
				if finance.total_amount+"00" == total_fee:
					finance.trade_status = True
					finance.receipt_amount = finance.total_amount
					try:
						lastfinance = Finance.objects.all().filter(products = finance.products, trade_status = True).order_by('-end')[0]
					except:
						lastfinance = None
					total_amount = int(finance.total_amount)
					if lastfinance:
						last_out_trade_no = lastfinance.end
					else:
						last_out_trade_no = 0
					productsid = str(finance.products.id)
					if len(productsid) == 1:
						productsid = "000"+productsid
					elif len(productsid) == 2:
						productsid = "00"+productsid
					elif len(productsid) == 3:
						productsid = "0"+productsid
					elif len(productsid) == 4:
						pass
					elif len(productsid) > 4:
						return HttpResponse("<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[None]]></return_msg></xml>")
					listb = str(last_out_trade_no + 1)
					listl = str(last_out_trade_no + total_amount )
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
						return HttpResponse("<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[None]]></return_msg></xml>")
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
						return HttpResponse("<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[None]]></return_msg></xml>")
					userlist = productsid + "_" + str(time.time()) + "_" + listb + "-" + listl
					userlist = userlist.replace('.', '')

					finance.out_trade_no = str(userlist)
					finance.start = int(listb)
					finance.end = int(listl)
					finance.save()

					products = finance.products
					products.one = int(listl)
					products.save(update_fields=['one'])

					updatenew = Updatenew(finance = finance)
					updatenew.save()


					return HttpResponse("<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[None]]></return_msg></xml>")
				else:
					return HttpResponse("<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[None]]></return_msg></xml>")
			except:
				return HttpResponse("<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[None]]></return_msg></xml>")
		else:
			return HttpResponse("<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[None]]></return_msg></xml>")
	except:
		return HttpResponse("<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[None]]></return_msg></xml>")




@login_required(login_url='/user/loggin/')
def alipayfinance(request):
	one = request.GET.get('one')
	productsid = request.GET.get('products')
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
		finance = Finance(user = request.user, out_trade_no = out_trade_no, total_amount = total_amount, products = products, start = int(listb), end = int(listl))
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

				try:
					lastfinance = Finance.objects.all().filter(products = finance.products, trade_status = True).order_by('-end')[0]
				except:
					lastfinance = None
				total_amount = int(finance.total_amount)
				if lastfinance:
					last_out_trade_no = lastfinance.end
				else:
					last_out_trade_no = 0
				productsid = str(finance.products.id)
				if len(productsid) == 1:
					productsid = "000"+productsid
				elif len(productsid) == 2:
					productsid = "00"+productsid
				elif len(productsid) == 3:
					productsid = "0"+productsid
				elif len(productsid) == 4:
					pass
				elif len(productsid) > 4:
					return HttpResponse("failure")
				listb = str(last_out_trade_no + 1)
				listl = str(last_out_trade_no + total_amount )
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
					return HttpResponse("failure")
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
					return HttpResponse("failure")
				userlist = productsid + "_" + str(time.time()) + "_" + listb + "-" + listl
				finance.out_trade_no = str(userlist)
				finance.start = int(listb)
				finance.end = int(listl)


				finance.save()
				products = finance.products
				products.one = int(listl) 
				products.save(update_fields=['one'])
				updatenew = Updatenew(finance = finance)
				updatenew.save()
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




def onebillpage(request, user_id):
	user = MyUser.objects.get(id = user_id)
	onebill = Finance.objects.filter(trade_status = True).filter(user = user).order_by('-id')
	context = {
		'onebill': onebill,
	}
	return render(request, 'onebillpage.html',  context)
