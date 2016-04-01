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
# Create your models here.
class Group(models.Model):
	#文章名称
	title = models.CharField(max_length=120)
	#文章上传时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	#文章更新时间
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
	#作者
	founder = models.ForeignKey(MyUser)
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
	#文章名称
	title = models.CharField(max_length=120)
	#文章上传时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	#文章更新时间
	updated = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	#作者
	writer = models.ForeignKey(MyUser)
	#文章内容
	content = RichTextUploadingField(max_length=5000)
	#文章地址
	url_address = models.CharField(max_length=500, null=True, blank=True)
	#文章图标
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	group = models.ForeignKey(Group)
	readers = models.IntegerField(default=0)
	#自定义查询语句
	#objects = ArticleManager()
	def __unicode__(self):
		return self.title

	def get_image_url(self):
		return "%s%s" %(settings.STATIC_URL, self.image)

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

class CollectionTopic(models.Model):
	user = models.ForeignKey(MyUser)
	topic = models.ForeignKey(Topic)


@receiver(post_delete, sender=Topic)
def subtopicount(sender, **kwargs):
    topic = kwargs.pop("instance")
    group = Group.objects.get(id =topic.group.id)
    group.topicount -= 1
    group.save()