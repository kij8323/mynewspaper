from django.contrib import admin

# Register your models here.
from .models import Updatenew
# Register your models here.

class UpdatenewAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'comment','payscore','timestamp', 'score','products')


admin.site.register(Updatenew, UpdatenewAdmin)
