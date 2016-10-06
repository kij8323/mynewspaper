from django.contrib import admin

# Register your models here.
from .models import Products, Application

class ProductsAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'amount', 'status', 'timestamp')
	class Meta:
		model = Products

class ApplicationAdmin(admin.ModelAdmin):
	list_display = ('id', 'products', 'user', 'get_userphone', 'get_useraddr', 'reason')
	class Meta:
		model = Application

admin.site.register(Products, ProductsAdmin)

admin.site.register(Application, ApplicationAdmin)
