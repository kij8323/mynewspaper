from django.contrib import admin


# Register your models here.
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender_object','recipient', 'text', 'verb')

admin.site.register(Notification, NotificationAdmin)
