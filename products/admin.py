from django.contrib import admin

# Register your models here.
from .models import Products, Application, Payscore, Payscorerec

class ProductsAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'amount', 'status', 'verify', 'timestamp')
	class Meta:
		model = Products

class ApplicationAdmin(admin.ModelAdmin):
	list_display = ('id', 'products', 'user', 'get_userphone', 'address', 'reason' , 'verify')
	class Meta:
		model = Application


class PayscoreAdmin(admin.ModelAdmin):
	list_display = ('id', 'products', 'user', 'payscore', 'timestamp')
	class Meta:
		model = Payscore


class PayscorerecAdmin(admin.ModelAdmin):
	list_display = ('id', 'products', 'user', 'payscore', 'timestamp')
	class Meta:
		model = Payscorerec


admin.site.register(Products, ProductsAdmin)

admin.site.register(Application, ApplicationAdmin)

admin.site.register(Payscore, PayscoreAdmin)

admin.site.register(Payscorerec, PayscorerecAdmin)
