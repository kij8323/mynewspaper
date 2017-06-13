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
from django.db.models.signals import pre_save, post_delete, post_save
from accounts.models import MyUser
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from products.models import Products
from DjangoUeditor.models import UEditorField
import os
from article.tasks import topicwritescore, instancesave
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

	#文章名称
	glyphicon = models.CharField(max_length=120, default='glyphicon-folder-open')


	def __unicode__(self):
		return self.title

	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.image)

	def blockid(self):
		blockid = "block"+str(self.id)
		return blockid

	def get_absolute_url(self):
		return reverse('group_detail', kwargs={"group_id": self.id})

class Groupmanager(models.Model):
	manager = models.ForeignKey(MyUser, default=2028)
	group = models.ForeignKey(Group)
		



class Topic(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	#文章名称
	title = models.CharField(max_length=120)

	associatetitle = models.CharField(max_length=120, null=True, blank=True)

	#文章上传时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	#文章更新时间
	updated = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	#作者
	writer = models.ForeignKey(MyUser, db_index=True)
	#文章内容
	content = UEditorField(max_length=150000, width=800, upload_settings={"imageMaxSize":1500000})
	#文章地址
	url_address = models.CharField(max_length=500, null=True, blank=True)
	group = models.ForeignKey(Group)
	readers = models.IntegerField(default=0)
	#是否为封面
	cover = models.BooleanField(default=False, db_index=True)
	#自定义查询语句
	products = models.ForeignKey(Products, null=True, blank=True, db_index=True)

	savetext = models.BooleanField(default=False, db_index=True)

	#是否为原创
	original = models.BooleanField(default=True, db_index=False)

	#是否为封面
	cover = models.BooleanField(default=False, db_index=True)

	#测评广告位
	guanggao = models.BooleanField(default=False, db_index=True)
	#积分
	score = models.BooleanField(default=False, db_index=True)



	#是否在测评页显示1张图
	img1 = models.BooleanField(default=False, db_index=True)
	#是否在测评页显示3张图
	img3 = models.BooleanField(default=False, db_index=True)

        #文章图标
        image = models.ImageField(upload_to='images/topic/', null=True, blank=True)

#首页推荐话题图
        imagesugg = models.ImageField(upload_to='images/topic/', null=True, blank=True)

	imagefst3 = models.ImageField(upload_to='images/topic/', null=True, blank=True)
	imagescd3 = models.ImageField(upload_to='images/topic/', null=True, blank=True)
	imagethd3 = models.ImageField(upload_to='images/topic/', null=True, blank=True)

	images1 = models.ImageField(upload_to='images/', null=True, blank=True)
	images2 = models.ImageField(upload_to='images/', null=True, blank=True)
	images3 = models.ImageField(upload_to='images/', null=True, blank=True)
	images4 = models.ImageField(upload_to='images/', null=True, blank=True)
	images5 = models.ImageField(upload_to='images/', null=True, blank=True)
	images6 = models.ImageField(upload_to='images/', null=True, blank=True)


	def get_imagefst3_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.imagefst3)

	def get_imagescd3_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.imagescd3)

	def get_imagethd3_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.imagethd3)

	#objects = ArticleManager()
	def __unicode__(self):
		return self.title

	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.image)

	def get_imagesugg_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.imagesugg)


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


	def get_image1_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.images1)

	def get_image2_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.images2)

	def get_image3_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.images3)

	def get_image4_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.images4)

	def get_image5_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.images5)

	def get_image6_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.images6)



class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'group', 'content']
        labels = {
            'title': _('标题'),
            'group': _('分类'),
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



#话题点赞
class TopicLike(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser)
	topic = models.ForeignKey(Topic)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)


#作者加积分
class TopicWriteScoreM(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser)
	topic = models.ForeignKey(Topic)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)



#评论者与作者同时加分
class Topicusercomment(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser)
	topic = models.ForeignKey(Topic)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)


#作者回复他人评论时，作者加10分
class Topicwritereply(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser)
	topic = models.ForeignKey(Topic)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)


#评论获他人回复
class Topiccommentreply(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user1 = models.ForeignKey(MyUser)
	user2 = models.ForeignKey(MyUser, related_name='otheruser')
	topic = models.ForeignKey(Topic)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)



#每删除一个话题，话题组的话题数量-1
@receiver(post_delete, sender=Topic)
def subtopicount(sender, **kwargs):
	topic = kwargs.pop("instance")
	group = Group.objects.get(id =topic.group.id)
	value = topic.group.id
	group.topicount -= 1
	group.save()
	cachekey = "group_topic_count_" + str(group.id)
	if cache.get(cachekey) != None:
		cache.decr(cachekey)
	else:
		group = Group.objects.get(id=value)
		cache.set(cachekey,  group.topicount)



#打卡
class Daka(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser)
	date = models.CharField(max_length=500)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)



@receiver(post_save, sender=Topic)
def subtopicount(sender, **kwargs):
	os.system('echo yes | python /home/shen/Documents/paperproject/mynewspaper/manage.py collectstatic')
	topic = kwargs.pop("instance")


@receiver(pre_save, sender=Topic)
def Updatenewscore(sender, **kwargs):
        topic = kwargs.pop("instance")
        try:
                topic1 = Topic.objects.get(id = topic.id)
                if topic.score == True and topic1.score == False and topic.savetext == False:
                        try:
                                topicwritescorem = TopicWriteScoreM.objects.get(topic=topic, user=topic.writer)
                        except:
                                topicwritescorem = None
                        if topicwritescorem:
                                pass
                        else:
                                topicwritescore.delay(topic.writer, topic, TopicWriteScoreM)

                else:
                        pass
        except:
                pass
