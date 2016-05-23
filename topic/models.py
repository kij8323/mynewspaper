#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from accounts.models import MyUser
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from accounts.models import MyUser
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
# Create your models here.
class Group(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	#文章名称
	title = models.CharField(max_length=120)
	#文章上传时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, db_index=True)
	#文章更新时间
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
	#作者
	founder = models.ForeignKey(MyUser, db_index=True)
	#副标题
	associatetitle = models.CharField(max_length=500, null=True, blank=True)
	#文章图标
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	topicount = models.IntegerField(default=0)

	def __unicode__(self):
		return self.title

	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.image)

	def blockid(self):
		blockid = "block"+str(self.id)
		return blockid

	def get_absolute_url(self):
		return reverse('group_detail', kwargs={"group_id": self.id})



class Topic(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	#文章名称
	title = models.CharField(max_length=120)
	#文章上传时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	#文章更新时间
	updated = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	#作者
	writer = models.ForeignKey(MyUser, db_index=True)
	#文章内容
	content = RichTextUploadingField(max_length=5000)
	#文章地址
	url_address = models.CharField(max_length=500, null=True, blank=True)
	#文章图标
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	group = models.ForeignKey(Group)
	readers = models.IntegerField(default=0)
	#是否为封面
	cover = models.BooleanField(default=False, db_index=True)
	#自定义查询语句
	#objects = ArticleManager()
	def __unicode__(self):
		return self.title

	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.image)

	def blockid(self):
		blockid = "block"+str(self.id)
		return blockid

	def get_absolute_url(self):
		return reverse('topic_detail', kwargs={"topic_id": self.id})

	def lastcommentime(self):
		return self.comment_set.all()[0:1].get()


		# return self.comment_set.all().order_by('-timestamp')[1]
		
	def test(self):
		return self.comment_set.all()




class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']
        labels = {
            'title': _('标题'),
            'content': _('内容'),
        }

# @receiver(pre_save, sender=Topic)
# def addtopicount(sender, **kwargs):
#     topic = kwargs.pop("instance")
#     group = Group.objects.get(id =topic.group.id)
#     group.topicount += 1
#     group.save()

#收藏的话题多对多
class CollectionTopic(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser, db_index=True)
	topic = models.ForeignKey(Topic, db_index=True)

#每删除一个话题，话题组的话题数量-1
@receiver(post_delete, sender=Topic)
def subtopicount(sender, **kwargs):
	topic = kwargs.pop("instance")
	group = Group.objects.get(id =topic.group.id)
	value = topic.group.id
	group.topicount -= 1
	group.save()
	cachekey = "group_topic_count_" + str(group.id)
	if cache.get(cachekey):
		cache.decr(cachekey)
	else:
		group = Group.objects.get(id=value)
		cache.set(cachekey,  group.topicount)
