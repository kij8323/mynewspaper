from django.contrib import admin

# Register your models here.

from .models import Company

class CompanyAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'industry', 'location', 'timestamp')
	class Meta:
		model = Company

admin.site.register(Company, CompanyAdmin)

