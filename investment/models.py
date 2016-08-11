#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from accounts.models import MyUser
from django.conf import settings
from django.core.urlresolvers import reverse
from ckeditor.fields import RichTextField
from django.forms import ModelForm

class Investment(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	#公司名称
	title = models.CharField(max_length=120)
	#公司名称en
	entitle = models.CharField(max_length=120, null=True, blank=True)
	#公司网址
	weburl = models.CharField(max_length=120)
	#成立时间
	fundtime = models.CharField(max_length=100, default='——')
	#投资案例
	investindex = models.IntegerField(default=0, db_index=True)
	#简介
	introduce = RichTextField(max_length=2000,null=True)
	#公司上传时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	#公司更新时间
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
	#logo
	logo = models.ImageField(upload_to='images/', blank=True, default='images/companylogo.png')
	#投资偏好1
	preference1 = models.CharField(max_length=100, default='——')
	#投资偏好2
	preference2 = models.CharField(max_length=100, null=True, blank=True)
	#投资偏好3
	preference3 = models.CharField(max_length=100, null=True, blank=True)
	#投资偏好4
	preference4 = models.CharField(max_length=100, null=True, blank=True)
	#投资偏好5
	preference5 = models.CharField(max_length=100, null=True, blank=True)
	#投资领域
	investfiled1 = models.CharField(max_length=100, default='——')
	#投资领域
	investfiled2 = models.CharField(max_length=100, null=True, blank=True)
	#投资领域
	investfiled3 = models.CharField(max_length=100, null=True, blank=True)
	#投资领域
	investfiled4 = models.CharField(max_length=100, null=True, blank=True)
	#投资领域
	investfiled5 = models.CharField(max_length=100, null=True, blank=True)
	#投资领域
	investfiled6 = models.CharField(max_length=100, null=True, blank=True)
	#投资领域
	investfiled7 = models.CharField(max_length=100, null=True, blank=True)
	#投资领域
	investfiled8 = models.CharField(max_length=100, null=True, blank=True)
	#投资领域
	investfiled9 = models.CharField(max_length=100, null=True, blank=True)


	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('investment_detail', kwargs={"investment_id": self.id})

	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.logo)


#收藏的话题多对多
class CollectionInvestment(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser, db_index=True)
	investment = models.ForeignKey(Investment, db_index=True)


class InvestmentBuiltForm(ModelForm):
    class Meta:
        model = Investment
        fields = ['title', 'weburl', 'fundtime', 'investindex', 'introduce', 'logo', 'preference1', 'preference2', 'preference3', 'preference4', 'preference5', 'investfiled1', 'investfiled2', 'investfiled3', 'investfiled4', 'investfiled5', 'investfiled6', 'investfiled7', 'investfiled8', 'investfiled9']
        labels = {
            'title': ('机构名称'),
            'weburl': ('网址'),
            'fundtime': ('成立时间'),
            'investindex': ('投资案例'),
            'introduce': ('简介'),
            'logo': ('标志'),
            'logo': ('标志'),
            'preference1': ('投资偏好1'),
            'preference2': ('投资偏好2'),
            'preference3': ('投资偏好3'),
            'preference4': ('投资偏好4'),
            'preference5': ('投资偏好5'),
            'investfiled1': ('投资领域1'),
            'investfiled2': ('投资领域2'),
            'investfiled3': ('投资领域3'),
            'investfiled4': ('投资领域4'),
            'investfiled5': ('投资领域5'),
            'investfiled6': ('投资领域6'),
            'investfiled7': ('投资领域7'),
            'investfiled8': ('投资领域8'),
            'investfiled9': ('投资领域9'),


        }
