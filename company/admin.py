from django.contrib import admin


# Register your models here.

from .models import Company, CollectionCompany

class CompanyAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'verify', 'industry', 'location', 'timestamp')
	class Meta:
		model = Company

class CollectionCompanyAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'company')
	class Meta:
		model = CollectionCompany

admin.site.register(Company, CompanyAdmin)

admin.site.register(CollectionCompany, CollectionCompanyAdmin)
