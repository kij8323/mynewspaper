#coding=utf-8
from django.db import models
from accounts.models import MyUser
from article.models import Article
from topic.models import Topic
from ckeditor.fields import RichTextField
from django.forms import ModelForm
# Create your models here.
class Comment(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	#发表评论用户
	user = models.ForeignKey(MyUser, db_index=True)
	#评论的父评论
	parent = models.ForeignKey("self", null=True, blank=True, db_index=True)
	#评论的视频
	article = models.ForeignKey(Article, null=True, blank=True, db_index=True)
	topic = models.ForeignKey(Topic, null=True, blank=True, db_index=True)
	#评论内容
	text = RichTextField(max_length=5000, null=True, blank=True)
	#评论发表时间
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, db_index=True)
	#评论修改时间
	updated = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
	is_privcycomment = models.BooleanField(default=False)
	#自定义查询
	# objects = CommentManager()
	#回复的评论用户
	reponse = models.CharField(max_length=255, null=True, blank=True)
	
	parenttext = models.TextField(null=True, blank=True)
	#计算回复热度
	readers = models.IntegerField(default=0)

	class Meta:
		ordering = ['-timestamp']

	def __unicode__(self):
		return self.user.username


	def is_child(self):
		if self.parent is not None:
			return True
		else:
			return False

	@property
	def like(self):
 		return CommentLike.objects.filter(comment=self).count()

	def dislike(self):
 		return CommentDisLike.objects.filter(comment=self).count()

	def child_comment(self):
 		return Comment.objects.filter(parent=self).order_by('timestamp')

	def child_commentcount(self):
 		return Comment.objects.filter(parent=self).count()

#text = RichTextField(max_length=5000, null=True, blank=True)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

#用户和评论之间的点赞多对多表
class CommentLike(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser, db_index=True)
	comment = models.ForeignKey(Comment, db_index=True)

#用户和评论之间的点衰多对多表
class CommentDisLike(models.Model):
	id = models.AutoField(primary_key=True, db_index=True)
	user = models.ForeignKey(MyUser, db_index=True)
	comment = models.ForeignKey(Comment, db_index=True)
