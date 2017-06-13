from django.contrib import admin

# Register your models here.

from .models import Comment, CommentLike, CommentDisLike

class CommentAdmin(admin.ModelAdmin):
	list_display = ('id', '__unicode__', 'readers', 'score', 'text', 'timestamp')
	class Meta:
		model = Comment

class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','comment')

class CommentDisLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','comment')

admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
admin.site.register(CommentDisLike, CommentDisLikeAdmin)
