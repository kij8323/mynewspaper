#coding=utf-8
from django.db import models

# Create your models here.
from topic.models import Topic
from comment.models import Comment
from products.models import Payscore, Products
from article.tasks import instancedelete, instancesave
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete, post_save
from datetime import timedelta 


# Create your models here.

class Updatenew(models.Model):
	products = models.ForeignKey(Products, null=True, blank=True)
	topic = models.ForeignKey(Topic, null=True, blank=True)
	comment = models.ForeignKey(Comment, null=True, blank=True)
	payscore = models.ForeignKey(Payscore, null=True, blank=True)
	score = models.BooleanField(default=False)
	#更新时间
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

@receiver(pre_save, sender=Products)
def Updatenewproducts(sender, **kwargs):
	products = kwargs.pop("instance")
	try:
		products1 = Products.objects.get(id = products.id)
		if products.verify == True and products1.verify == False and products1.status == 1:
			updatenew = Updatenew(products = products1)
			instancesave.delay(updatenew)
		else:
			pass
	except:
		pass



@receiver(post_save, sender=Comment)
def Updatenewcomment(sender, **kwargs):
	comment = kwargs.pop("instance")
	if comment.updated - comment.timestamp > timedelta(seconds=0.01):
		pass
	else:
		updatenew = Updatenew(comment = comment)
		instancesave.delay(updatenew)

@receiver(post_save, sender=Topic)
def Updatenewtopic(sender, **kwargs):
	topic = kwargs.pop("instance")
	if topic.savetext == False and topic.readers == 0:
		updatenew = Updatenew(topic = topic)
		instancesave.delay(updatenew)
	else:
		pass



@receiver(pre_save, sender=Topic)
def Updatenewscore(sender, **kwargs):
	topic = kwargs.pop("instance")
	try:
		topic1 = Topic.objects.get(id = topic.id)
		if topic.score == True and topic1.score == False and topic.savetext == False:
			updatenew = Updatenew(topic = topic1, score = True)
			instancesave.delay(updatenew)
		else:
			pass
	except:
		pass



@receiver(post_save, sender=Payscore)
def Updatenewpayscore(sender, **kwargs):
	payscore = kwargs.pop("instance")
	updatenew = Updatenew(payscore = payscore)
	instancesave.delay(updatenew)

