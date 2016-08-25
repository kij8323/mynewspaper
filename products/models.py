#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from accounts.models import MyUser
from company.models import Company
from django.conf import settings
from django.core.urlresolvers import reverse
from ckeditor.fields import RichTextField
from django.utils import timezone




class Products(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	#产品名称
	title = models.CharField(max_length=120)
	#产品介绍
	introduction = RichTextField(max_length=20000,null=True)
	#产品价格
	price = models.IntegerField(default=0)
	#产品数量
	amount = models.IntegerField(default=0)
	#是否审核通过
	verify = models.BooleanField(default=False, db_index=True)
	#产品状态
	status = models.IntegerField(default=1)
	#第多少期试用
	periods = models.IntegerField(default=1)
	#产品图片
	picture = models.ImageField(upload_to='images/', blank=True, default='images/companylogo.png')

	#公司上传时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	# #公司更新时间
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

	#公司上传时间
	timedeadline = models.DateTimeField(null=True)

	company = models.ForeignKey(Company, null=True, blank=True)


	def __unicode__(self):
	    return self.title

	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.picture)

	def ret_timesince_sec(self):
		return (self.timedeadline - timezone.now()).days*24*60*60 + (self.timedeadline - timezone.now()).seconds

	def get_absolute_url(self):
		return reverse('products_detail', kwargs={"products_id": self.id})

#用户申请
class Application(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser)
	products = models.ForeignKey(Products)
	#是否中奖
	verify = models.BooleanField(default=False, db_index=True)
