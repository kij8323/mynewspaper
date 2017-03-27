#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from .signals import notify
from ckeditor.fields import RichTextField
from comment.models import Comment
from accounts.models import MyUser
from article.models import Article
from topic.models import Topic
import traceback 
from django.core.cache import cache
from django.conf import settings
from article.tasks import readersin, add, readersout, instancedelete, instancesave
from products.models import Products

# Create your models here.
class Notification(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	sender_object = models.ForeignKey(MyUser, db_index=True)#发送消息的用户
	verb = models.CharField(max_length=255, db_index=True)#发送消息的动作：@是@消息，_@_是私信
	#评论内容
	text = RichTextField(max_length=5000, null=True, blank=True)#消息内容
	target_article = models.ForeignKey(Article, null=True, blank=True)#产生消息的评论的文章
	target_topic = models.ForeignKey(Topic, null=True, blank=True)#产生消息的评论的话题
	#目标对象
	target_object = models.ForeignKey(Comment, null=True, blank=True)
	recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', db_index=True)
	#是否已读
	read = models.BooleanField(default=False)
	target_products = models.ForeignKey(Products, null=True, blank=True)#产生消息的评论的话题

	#消息发送时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=True)

	def setread(self):
		self.read = True
		instancesave.delay(self)
		cachekey = "user_unread_count" + str(self.recipient.id)
		if cache.get(cachekey) != None:
			cache.decr(cachekey)
			pass
		else:
			unread = Notification.objects.filter(recipient = self.recipient).filter(read = False).count()
			cache.set(cachekey,  unread, settings.CACHE_EXPIRETIME)
			pass
		if self.verb == '_@_':
			cachekey = "user_privcyunread_count" + str(self.recipient.id)
			if cache.get(cachekey) != None:
				cache.decr(cachekey)
				pass
			else:
				unread = Notification.objects.filter(recipient = self.recipient).filter(read = False).filter(verb = '_@_').count()
				cache.set(cachekey,  unread, settings.CACHE_EXPIRETIME)
				pass
		else:
			pass
		return ''


	def __unicode__(self):
		if self.target_object:
			context = {
				"sender": self.sender_object,
				"verb": self.verb,
				"target": self.target_object.text,
				"text": self.text,
				"recipient": self.recipient
			}
			return "%(sender)s %(verb)s %(recipient)s %(target)s  %(text)s" %context
		else:
			context = {
				"sender": self.sender_object,
				"verb": self.verb,
				"text": self.text,
				"recipient": self.recipient
			}
			return "%(sender)s %(verb)s %(recipient)s  %(text)s" %context

#通过notify.send生成新的消息
def new_notification(sender, **kwargs):
	kwargs.pop('signal', None)
	target_object = kwargs.pop("target_object", None)
	text = kwargs.pop("text")
	verb = kwargs.pop("verb")
	sender_object = sender
	recipient = kwargs.pop("recipient")
	target_article = kwargs.pop("target_article", None)
	target_topic = kwargs.pop("target_topic", None)
	target_products = kwargs.pop("target_products", None)
	try:
		c = Notification(target_object=target_object, 
						sender_object=sender_object, 
						target_topic=target_topic,
						target_article = target_article,
						target_products = target_products,
						recipient=recipient,
						verb = verb,
						text = text,
						)
		instancesave.delay(c)
	except:
		traceback.print_exc()

notify.connect(new_notification)
