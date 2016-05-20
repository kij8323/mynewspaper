#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from accounts.models import MyUser
from django.core.urlresolvers import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.core.cache import cache

# 文章
class Article(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	#文章名称
	title = models.CharField(max_length=120)
	associatetitle = models.CharField(max_length=120)
	#文章上传时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, db_index=True)
	#timestamp = models.DateTimeField('date published')
	# #文章更新时间
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
	#文章内容
	content = RichTextUploadingField(max_length=5000, null=True, blank=True)
	#作者
	writer = models.ForeignKey(MyUser, db_index=True)
	#转载
	fromner = models.TextField(max_length=500, null=True, blank=True)
	#文章地址
	url_address = models.CharField(max_length=500, null=True, blank=True)
	#文章图标
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	#文章图标是否显示在文章内容中
	images_show = models.BooleanField(default=False)
	#是否为封面
	cover = models.BooleanField(default=False, db_index=True)
	#计算文章热度
	readers = models.IntegerField(default=0, db_index=True)


	def __unicode__(self):
		return self.title

	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.image)

	def blockid(self):
		blockid = "block"+str(self.id)
		return blockid

	def get_absolute_url(self):
		return reverse('article_detail', kwargs={"article_id": self.id})

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
	#image_detail = models.ImageField(upload_to='static/images/', null=True, blank=True)
	#类别生成时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	#类别更新时间
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	#自定义查询
	#类别通过relations表与文章多对多
	relations = models.ManyToManyField(Article, through='Relation', )

	def __unicode__(self):
		return self.title
		
	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.image)

	def get_absolute_url(self):
		return reverse('category_detail', kwargs={"category_id": self.id})

#类别与文章的多对多关系表
class Relation(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	category = models.ForeignKey(Category, db_index=True)
	article = models.ForeignKey(Article, db_index=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, db_index=True)

#用户与文章之间的多对多收藏关系
class Collection(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser, db_index=True)
	article = models.ForeignKey(Article, db_index=True)

#每个文章实例生成，都会自动添加分类到id=3的类别
@receiver(post_save, sender=Article)
def categoryofarticle(sender, **kwargs):
    article = kwargs.pop("instance")
    try: 
    	thisrelationtag = Relation.objects.get(article=article)
    except:
    	thisrelationtag = False
    if thisrelationtag: #如果文章已经被分类直接返回
    	return;
    else:	#如果文章未分类则直接分类
		category = Category.objects.get(id = 7)
		relation = Relation(article= article, category = category)
		relation.save()
		os.system('echo yes | python /home/shen/Documents/paperproject/mynewspaper/manage.py collectstatic')
		cachekey = "writer_articlecount_" + str(article.writer.id)
		if cache.get(cachekey):
			cache.incr(cachekey)
		else:
			numwriter = article.writer.article_set.count()
			cache.set(cachekey, numwriter)
		# cachekey = "article_readers_" + str(article.id)
		# cache.set(cachekey, 0)
		# cache.incr(cachekey)
		# print cache.get(cachekey)

