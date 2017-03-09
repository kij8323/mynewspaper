from django.contrib import admin


# Register your models here.

from .models import Topiccommentreply,  Topicwritereply, Topicusercomment, TopicWriteScoreM, TopicLike, Group, Topic, CollectionTopic, Groupmanager

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','timestamp')

class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','timestamp', 'readers', 'savetext', 'cover', 'guanggao', 'score', 'group')

class CollectionTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','topic')

class GroupmanagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'manager','group')

class TopicLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','topic', 'timestamp')


class TopicWriteScoreMAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','topic', 'timestamp')

class TopicusercommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','topic', 'timestamp')

class TopicwritereplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','topic', 'timestamp')

class TopiccommentreplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user1','topic', 'timestamp', 'user2')



admin.site.register(Group, GroupAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(CollectionTopic, CollectionTopicAdmin)
admin.site.register(Groupmanager, GroupmanagerAdmin)
admin.site.register(TopicLike, TopicLikeAdmin)

admin.site.register(TopicWriteScoreM, TopicWriteScoreMAdmin)
admin.site.register(Topicusercomment, TopicusercommentAdmin)
admin.site.register(Topicwritereply, TopicwritereplyAdmin)
admin.site.register(Topiccommentreply, TopiccommentreplyAdmin)
