from django.contrib import admin

# Register your models here.
from .models import Scorebill

# Register your models here.
class ScorebillAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'score', 'plus', 'way')

admin.site.register(Scorebill, ScorebillAdmin)
