from django.contrib import admin

# Register your models here.

from .models import Article, Category, Relation, Collection

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','cover', 'original','deep','timestamp','readers')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','timestamp')

class RelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'category','article','timestamp')

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','article')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(Collection, CollectionAdmin)
#admin.site.register(Relation)
#admin.site.register(Article)Collection
