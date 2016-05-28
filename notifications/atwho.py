#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re, sys
from notifications.signals import notify
from accounts.models import MyUser
reload(sys)
sys.setdefaultencoding( "utf-8" )
from django.core.cache import cache
from django.conf import settings

#给评论中每一个被@的用户发送notifications，并返回一个被@用户的列表
def atwho(text, sender, targetcomment, targetarticle, targetopic):
	commmentdecode = text.decode("utf8")
	pattern = re.compile(u'@([\u4e00-\u9fa5\w\-]+)') 
	results =  pattern.findall(commmentdecode) #用正则把评论中有@的字符串分割开
	userlist = []
	for item in results:
		try:
			user = MyUser.objects.get(username = item.encode('utf8'))
		except:
			user = None
		if user:
			user = MyUser.objects.get(username = item.encode('utf8'))
			notify.send(sender=sender, target_object=targetcomment
					, recipient = user, verb="@"
					, text=text, target_article = targetarticle
					, target_topic = targetopic)
			cachekey = "user_unread_count" + str(user.id)
			if cache.get(cachekey) != None:
				cache.incr(cachekey)
			else:
				unread = Notification.objects.filter(recipient = self.recipient).filter(read = False).count()
				cache.set(cachekey,  unread, settings.CACHE_EXPIRETIME)
			userlist.append(item.encode('utf8'))
	return userlist


# def atwhononoti(text):
# 	commmentdecode = text.decode("utf8")
# 	pattern = re.compile(u'@([\u4e00-\u9fa5\w\-]+)')  
# 	results =  pattern.findall(commmentdecode) 
# 	userlist = []
# 	for item in results:
# 		user = MyUser.objects.filter(username = item.encode('utf8'))
# 		if user:
# 			user = MyUser.objects.get(username = item.encode('utf8'))
# 			#notify.send(sender=sender, target_object=targetcomment, recipient = user, verb="@", text=text)
# 			userlist.append('@'+item.encode('utf8')+' ')
# 	return userlist
