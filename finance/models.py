from django.db import models
from accounts.models import MyUser
from products.models import Products
# Create your models here.
class Finance(models.Model):
	out_trade_no =  models.CharField(max_length=64, null=True, blank=True)
	user = models.ForeignKey(MyUser, null=True, blank=True)
	products = models.ForeignKey(Products, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	trade_status = models.BooleanField(default=False)
	total_amount = models.CharField(max_length=100, null=True, blank=True)
	receipt_amount = models.CharField(max_length=100, null=True, blank=True)
	buyer_id =  models.CharField(max_length=16, null=True, blank=True)
	trade_no =  models.CharField(max_length=64, null=True, blank=True)
	out_biz_no =   models.CharField(max_length=64, null=True, blank=True)
