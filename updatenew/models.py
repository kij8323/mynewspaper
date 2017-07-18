#coding=utf-8
from django.db import models

# Create your models here.
from topic.models import Topic, TopicWriteScoreM
from comment.models import Comment
from products.models import Payscore, Products
from article.tasks import instancedelete, instancesave
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete, post_save
from datetime import timedelta 
from article.tasks import topicwritescore, instancesave, commentscore
from judgement.models import Instrument
from finance.models import Finance

# Create your models here.

class Updatenew(models.Model):
	products = models.ForeignKey(Products, null=True, blank=True)
	topic = models.ForeignKey(Topic, null=True, blank=True)
	comment = models.ForeignKey(Comment, null=True, blank=True)
	payscore = models.ForeignKey(Payscore, null=True, blank=True)
	instrument = models.ForeignKey(Instrument, null=True, blank=True)
	score = models.BooleanField(default=False)
	finance = models.ForeignKey(Finance, null=True, blank=True)
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


@receiver(post_save, sender=Instrument)
def Updatenewinstrument(sender, **kwargs):
	instrument = kwargs.pop("instance")
	if instrument.verify == True and instrument.grade == 0:
		updatenew = Updatenew(instrument = instrument)
		instancesave.delay(updatenew)
	else:
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





#评论被选为最佳
@receiver(pre_save, sender=Comment)
def Updatenewscore(sender, **kwargs):
	comment = kwargs.pop("instance")
	try:
		comment1 = Comment.objects.get(id = comment.id)
		if comment.score == True and comment1.score == False:
			comment.readers = comment.readers+30
			commentscore.delay(comment.user, comment)
		else:
			pass
	except:
		pass

@receiver(post_save, sender=Payscore)
def Updatenewpayscore(sender, **kwargs):
	payscore = kwargs.pop("instance")
	if payscore.win == False:
		updatenew = Updatenew(payscore = payscore)
		instancesave.delay(updatenew)
	else:
		pass
