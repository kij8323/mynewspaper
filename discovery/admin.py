from django.contrib import admin

from .models import Discovery, Discoveryhost


class DiscoveryAdmin(admin.ModelAdmin):
	list_display = ('id', 'host', 'title', 'timestamp', 'verify')

class DiscoveryhostAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'timestamp', 'updated')


admin.site.register(Discovery, DiscoveryAdmin)
admin.site.register(Discoveryhost, DiscoveryhostAdmin)



