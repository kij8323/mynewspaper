from django.db import models

# Create your models here.
from topic.models import Topic
from comment.models import Comment
from accounts.models import MyUser
from products.models import Products
# Create your models here.

class Scorebill(models.Model):
	user = models.ForeignKey(MyUser, db_index=True)
	score = models.IntegerField(default=0)
	plus = models.BooleanField(default=True)
	way = models.IntegerField(default=0)
	topic = models.ForeignKey(Topic, null=True, blank=True)
	comment = models.ForeignKey(Comment, null=True, blank=True)
	products = models.ForeignKey(Products, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

