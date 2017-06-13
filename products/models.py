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
from ckeditor_uploader.fields import RichTextUploadingField
from DjangoUeditor.models import UEditorField
from article.tasks import instancedelete, instancesave
from django.dispatch import receiver
from django.db.models.signals import post_save
import scorebill

class Products(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	#产品名称
	title = models.CharField(max_length=120)
	#产品介绍
	introduction = UEditorField(max_length=30000, width=800, upload_settings={"imageMaxSize":30204000}) 
	#产品价格
	price = models.CharField(max_length=100, null=True, blank=True)
	#产品数量
	amount = models.IntegerField(default=0)
	#积分竞拍数量
	scoreamount = models.IntegerField(default=0)
	#试用数量
	tryamount = models.IntegerField(default=0)

	#一元购数量
	oneamount = models.IntegerField(default=0)

	#是否积分竞拍
	ifscore = models.BooleanField(default=False, db_index=True)


	#是否参与申请
	ifapply = models.BooleanField(default=False, db_index=True)
	#是否一元购
	ifone = models.BooleanField(default=False, db_index=True)

	#积分当前价
	scoreing = models.IntegerField(default=0)
	#是否审核通过
	verify = models.BooleanField(default=False, db_index=True)
	#产品状态
	status = models.IntegerField(default=1)
	#第多少期试用
	periods = models.IntegerField(default=1)
	#报告数量
	reportnum = models.IntegerField(default=0)
	#产品图片
	picture = models.ImageField(upload_to='images/', blank=True, default='images/companylogo.png')

	#产品首页图片
	picturehome = models.ImageField(upload_to='images/', blank=True, default='images/companylogo.png')

	#pc端产品页展示
	picturedetail = models.ImageField(upload_to='images/', blank=True, default='images/companylogo.png')



	#公司上传时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	# #公司更新时间
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

	#公司上传时间
	timedeadline = models.DateTimeField(null=True)

	company = models.ForeignKey(Company, null=True, blank=True)

	#假申请人数
	applyamountcount = models.IntegerField(default=0)

	one = models.IntegerField(default=0)


	def __unicode__(self):
	    return self.title

	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.picture)

	def get_homeimage_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.picturehome)

	def get_detailimage_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.picturedetail)


	def ret_timesince_sec(self):
		return (self.timedeadline - timezone.now()).days*24*60*60 + (self.timedeadline - timezone.now()).seconds

	def ret_timesince_day(self):
		return (self.timedeadline - timezone.now()).days

	def get_absolute_url(self):
		return reverse('products_detail', kwargs={"products_id": self.id})

	def get_apply_url(self):
		return reverse('productsapply', kwargs={"products_id": self.id})

	def get_report_url(self):
		return reverse('productsreport', kwargs={"products_id": self.id})

	def get_payscore_url(self):
		return reverse('payscorerecord', kwargs={"products_id": self.id})



#用户申请
class Application(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser)
	products = models.ForeignKey(Products)
	reason = models.CharField(max_length=1000, null=True, blank=True)
	#是否中奖
	verify = models.BooleanField(default=False, db_index=True)
	address = models.CharField(max_length=200, null=True, blank=True)

	def get_userphone(self):
	    return self.user.phonenumber

	def get_useraddr(self):
	    return self.user.address



#积分竞拍
class Payscore(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser)
	products = models.ForeignKey(Products)
	payscore = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	#是否竞拍成功
	win = models.BooleanField(default=False)
	def __unicode__(self):
	    return self.products.title


#积分计算
class Payscorerec(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser)
	products = models.ForeignKey(Products)
	payscore = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)



@receiver(post_save, sender=Products)
def ppayscorerec(sender, **kwargs):
	products = kwargs.pop("instance")
	if products.status == 2:
		payscorerec = Payscorerec.objects.filter(products=products)
		for item in payscorerec:
			item.user.score = item.user.score + item.payscore
			instancesave.delay(item.user)
			instancedelete.delay(item)
			sb = scorebill.models.Scorebill(user = item.user, score = item.payscore, plus = True, way = 9, products = products)
			instancesave.delay(sb)
	else:
		pass;

