from django.contrib import admin


from .models import Instrumentgrade, Instrument, Category, Instrumentusercomment


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'model', 'verify', 'uper')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class InstrumentusercommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'instrument')


class InstrumentgradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'instrument', 'starall')

admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Instrumentusercomment, InstrumentusercommentAdmin)
admin.site.register(Instrumentgrade, InstrumentgradeAdmin)
