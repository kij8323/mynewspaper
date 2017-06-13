#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from company.models import Company
from django.conf import settings
from accounts.models import MyUser
from django.core.urlresolvers import reverse

import os
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete, post_save


#分类
class Category(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	#类别名称
	title = models.CharField(max_length=120)
	#类别描述
	description = models.TextField(max_length=5000, null=True, blank=True)
	introduction = models.TextField(max_length=5000, null=True, blank=True)
	#类别图标
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	#类别生成时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	#类别更新时间
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)


	def __unicode__(self):
		return self.title

# Create your models here.
class Instrument(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	#分类
	category = models.ForeignKey(Category, null=True, blank=True)
	#设备型号
	model = models.CharField(max_length=120)

	#生产厂家
	usercompany = models.CharField(max_length=120, null=True, blank=True)

	uper = models.ForeignKey(MyUser, null=True, blank=True)

	#生产厂家
	company = models.ForeignKey(Company, null=True, blank=True)
	#产品图标
	image = models.ImageField(upload_to='images/Instrument/', null=True, blank=True)
	#是否审核通过
	verify = models.BooleanField(default=False, db_index=True)
	#官网地址
	introaddr = models.CharField(max_length=500, null=True, blank=True)
	#评分
	grade = models.IntegerField(default=0)
	#上市时间
	uptime = models.CharField(max_length=500, null=True, blank=True)


	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	updated = models.DateTimeField(auto_now_add=False, auto_now=True)


	def __unicode__(self):
		return self.model

	def get_absolute_url(self):
		return reverse('instrument_detail', kwargs={"instrument_id": self.id})


	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.image)




#评论作者加分
class Instrumentusercomment(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser)
	instrument = models.ForeignKey(Instrument)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)


#评论作者加分
class Instrumentgrade(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	instrument = models.ForeignKey(Instrument)
	starall = models.IntegerField(default=0)
	star1 = models.IntegerField(default=0)
	star2 = models.IntegerField(default=0)
	star3 = models.IntegerField(default=0)
	star4 = models.IntegerField(default=0)
	star5 = models.IntegerField(default=0)
	grade = models.IntegerField(default=0)


@receiver(post_save, sender=Instrument)
def instrusave(sender, **kwargs):
	os.system('echo yes | python /home/shen/Documents/paperproject/mynewspaper/manage.py collectstatic')

