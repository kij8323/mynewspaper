from django.db import models
from accounts.models import MyUser
from products.models import Products
from django.conf import settings
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
	out_biz_no =   models.CharField(max_length=6400, null=True, blank=True)
	qrcodeimage = models.ImageField(upload_to='images/qrcode/', null=True, blank=True)

	start = models.IntegerField(default=0)
	end = models.IntegerField(default=0)


	way = models.CharField(max_length=100, null=True, blank=True)
	refund = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=28, null=True, blank=True)



	def __unicode__(self):
		return self.out_trade_no

	def get_qrcodeimage_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.qrcodeimage)
