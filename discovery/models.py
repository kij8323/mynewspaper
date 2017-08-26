from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
# Create your models here.

class Discoveryhost(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	icon = models.ImageField(upload_to='discovery/img/', null=True, blank=True, default='images/78avatarbig.jpg')
	title = models.CharField(max_length=120)
	addr = models.CharField(max_length=1200)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

	def __unicode__(self):
	    return self.title
	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.icon)
	def get_absolute_url(self):
		return reverse('discoverycategory', kwargs={"category_id": self.id})



class Discovery(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	host = models.ForeignKey(Discoveryhost)
	img = models.CharField(null=True, blank=True, max_length=1000)
	title = models.CharField(max_length=120)
	count = models.CharField(max_length=120)
	addr = models.CharField(max_length=1200)
	price = models.CharField(max_length=120)
	infor = models.CharField(max_length=120, null=True, blank=True)
	amount = models.CharField(max_length=120)
	verify = models.BooleanField(default=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
	def __unicode__(self):
	    return self.title

	def get_image_url(self):
		return "%s" %(self.img)
