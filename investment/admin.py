from django.contrib import admin

# Register your models here.


from .models import Investment, CollectionInvestment

class InvestmentAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'investindex')
	class Meta:
		model = Investment

class CollectionInvestmentAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'investment')
	class Meta:
		model = CollectionInvestment

admin.site.register(Investment, InvestmentAdmin)

admin.site.register(CollectionInvestment, CollectionInvestmentAdmin)
