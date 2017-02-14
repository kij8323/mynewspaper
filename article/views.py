#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from .models import Article, Category, Relation, Collection
from .form import CommentForm
from comment.models import Comment, CommentLike, CommentDisLike
import traceback  
import types  
import json
from django.http import HttpResponse
from notifications.signals import notify
from accounts.models import MyUser
from notifications.atwho import atwho
from itertools import chain
import datetime
from datetime import timedelta
from django.core.cache import cache
from article.tasks import commentzanplus, commentzanminus,  readersin, add, readersout, instancedelete, instancesave

from django.conf import settings
ARTICLE_DETAIL_RIGHTSIDERANK_TIMERANGE = 100 #article_detail页面右边栏按readers排序文章的时间范围
ARTICLE_DETAIL_REALATIONARTICLE_COUNT = 3  #article_detail页面底部相关文章数量
ARTICLE_DETAIL_HOTCOMMENT_READERSRANGE = 3 #最热回复的门限制

#文章页面
def article_detail(request, article_id):
	try:
		article = Article.objects.get(pk=article_id)
		#文章回复数
		#numofcomment = article.comment_set.count()
		#作者文章总数
		#numwriter = article.writer.article_set.count()
		#文章所有类别
		#category = Category.objects.all()
		#作者所有文章总阅读数
		# numreaders = 0
		# for x in article.writer.article_set.all():
		# 	numreaders = x.readers + numreaders

	except Article.DoesNotExist:
		raise Http404("Article does not exist")
	#阅读数+1
	# article.readers += 1
	# article.save()
	#阅读数+1,将readers+1的操作放到celery中，加快网页的加载时间
	readersin.delay(article)
	#缓存的readers 增加1
	cachekey = "article_readers_" + str(article_id)
	if cache.get(cachekey) != None:
		cache.incr(cachekey)
	#	print cache.incr(cachekey)
	else:
	#	print 'test'
		cache.set(cachekey, article.readers, settings.CACHE_EXPIRETIME)

	#当前读者对象
	user = request.user
	#读者是否收藏该文章
	try:
		collection = Collection.objects.get(article=article, user=user.id)
		collection = '已收藏'
	except:
		collection = '收藏'
	# if collection: 
	# 	collection = '已收藏'
	# else:
	# 	collection = '收藏'
	#评论按热度排序
	commentorderbyreaders = Comment.objects.filter(article=article).filter(readers__gt=ARTICLE_DETAIL_HOTCOMMENT_READERSRANGE).order_by('-readers')[0:3]
	#commentorderbyreaderscount = commentorderbyreaders.count()
	#文章回复按时间
	comment = Comment.objects.filter(article=article).order_by('-timestamp')
	#文章回复数大于5才有更多回复按钮
	if comment.count() > 5:
		moercomment = True
	else:
		moercomment = False#链接最热回复和按时间排序的回复
	#链接热度排序和时间排序回复
	# comment = list(chain(commentorderbyreaders, comment))
	# comment = sorted(set(comment), key=comment.index) 
	#显示头5个回复
	comment = comment[:5]
	#把本页地址装入session
	request.session['lastpage'] = request.get_full_path()
	#分享链接的地址
	sharelink = request.get_host()+request.get_full_path()

	print sharelink
	#文章属于哪些类别
	thisrelationtag = Relation.objects.filter(article=article)
	print thisrelationtag[0].category
	#右边栏文章统一类的按readers排序
	hotarticle = Article.objects.all().filter(timestamp__gte=datetime.date.today() - timedelta(days=ARTICLE_DETAIL_RIGHTSIDERANK_TIMERANGE)).filter(category=thisrelationtag[0].category).exclude(id = article.id).order_by('-readers')[:5]
	#统一类的按timestamp排序文章
	thisrelationtagarticle = Relation.objects.filter(category=thisrelationtag[0].category).exclude(article = article).order_by('-timestamp')
#	if thisrelationtagarticle.count()==0:#如果类别中除了自己就没有其他的文章了，就需要从另外的列别中查找文章
#		thisrelationtagarticle = Relation.objects.filter(category=thisrelationtag[1].category).exclude(article = article).order_by('-timestamp')
#	if thisrelationtagarticle.count()==0:
#		thisrelationtagarticle = Relation.objects.filter(category=thisrelationtag[2].category).exclude(article = article).order_by('-timestamp')
	#文章被多少人收藏过
	#usercollectioncount = Collection.objects.filter(article=article).count()
	context = {
		'article':article,
		'user':user,
		"form": CommentForm,
		#"submit_btn": "发表",
		"comment": comment,
		#'numofcomment': numofcomment,
		#'numwriter': numwriter,
		#'numreaders': numreaders,
		'hotarticle': hotarticle,
		#'category': category,
		'moercomment': moercomment,
		'collection' : collection,
		'thisrelationtag' : thisrelationtag,
		'thisrelationtagarticle': thisrelationtagarticle[0:ARTICLE_DETAIL_REALATIONARTICLE_COUNT], 
		#'usercollectioncount' : usercollectioncount, 
		'sharelink': sharelink,
		"commentorderbyreaders": commentorderbyreaders,
	}
	return render(request, 'article_detail.html',  context)



#分类文章页面
def category_detail(request, category_id):
	try:
		category = Category.objects.get(pk=category_id)
		articlequery = Relation.objects.filter(category=category).order_by('-article_id')[0:5]#显示该类别最新的5篇文章
		categoryquery = Category.objects.all
	except Category.DoesNotExist:
		raise Http404("Category does not exist")
	context = {
		'articlequery': articlequery,
		'categorytitle': category.title,
		'categoryquery': categoryquery,
	}
	return render(request, 'category_detail.html',  context)

def category_all(request):
	try:
		#category = Category.objects.get(pk=category_id)
		articlequery = Relation.objects.all().order_by('-article_id')[0:5]#显示该类别最新的5篇文章
		#categoryquery = Category.objects.all
	except Category.DoesNotExist:
		raise Http404("Category does not exist")
	context = {
		'articlequery': articlequery,
		'categorytitle': "资讯",
		# 'categoryquery': categoryquery,
	}
	return render(request, 'category_all.html',  context)

#ajax，文章评论
def articlecomment(request):
	if request.is_ajax() and request.method == 'POST':
		text = request.POST.get('comment')#评论的内容
		articleid = request.POST.get('articleid')
		article = Article.objects.get(pk=articleid)
		user = request.user
		try:
			c = Comment(user=user, article=article, text=text)
			c.save()
			#文章回复数量redis缓存 增加1
			cachekey = "article_comment_" + str(articleid)
			if cache.get(cachekey) != None:
				cache.incr(cachekey)
			else:
				cache.set(cachekey, article.comment_set.count(), settings.CACHE_EXPIRETIME)
			#返回@用户的列表，并向@的用户发送消息
			userlist = atwho(text = text, sender = user
							, targetcomment = c, targetarticle = article, targetproducts = None
							, targetopic = None)
			#给被@的用户增加链接
			for item in userlist:
				print 'for item in userlist:'
				atwhouser = MyUser.objects.get(username = item)
#				test = "@<a href='" +'/user/'+str(atwhouser.id)+'/informations/'+"'>"+atwhouser.username+"</a>"+' '
#				text = text.replace('@'+item+' ', test);
				test = "@<a href='" +'/user/'+str(atwhouser.id)+'/informations/'+"'>"+atwhouser.username+"</a>"+' '
				test1 = "@<a href='" +'/user/'+str(atwhouser.id)+'/informations/'+"'>"+atwhouser.username+"</a>"+'&nbsp;'
				text = text.replace('@'+item+' ', test);
				text = text.replace('@'+item+'&nbsp;', test1);
			cachekey = "comment_user_count_" + str(user.id)
			if cache.get(cachekey) != None:
				cache.incr(cachekey)
			else:
				usercomnum = Comment.objects.filter(user = user).count()
				cache.set(cachekey,  usercomnum)
			data = {
			"user": user.username,
			"text": text,
			"commentid": c.id
			}
			json_data = json.dumps(data)
			return HttpResponse(json_data, content_type='application/json')
		except:
			traceback.print_exc()
			raise Http404(traceback)
	else:
		raise Http404


#ajax，评论的评论
def commentcomment(request):
	if request.is_ajax() and request.method == 'POST':
		print 'commentcomment'
		text = request.POST.get('comment')
		articleid = request.POST.get('articleid')
		#parenttext = request.POST.get('parenttext')
		preentid = request.POST.get('preentid')
		article = Article.objects.get(pk=articleid)
		#comment = Comment.objects.filter(article=article)
		targetcomment = Comment.objects.get(pk=preentid)
		user = request.user
		if targetcomment.user == user:
			pass;
		else:
			receiver = targetcomment.user.username
			text="@"+receiver+" "+text
		try:
			c = Comment(user=user, article=article, text=text, parent=targetcomment)
			c.save()
			#文章回复数量缓存 增加1
			cachekey = "article_comment_" + str(articleid)
			if cache.get(cachekey) != None:
				cache.incr(cachekey)
			else:
				cache.set(cachekey, article.comment_set.count(), settings.CACHE_EXPIRETIME)
			#被评论的评论readers+1放到消息队列中
			readersin.delay(targetcomment)
			#返回@用户的列表，并向@的用户发送消息
			userlist = atwho(text = text, sender = user, targetcomment = c, targetproducts = None
							, targetarticle = article, targetopic = None )
			#给被@的用户增加链接
			for item in userlist:
				print 'for item in userlist:'
				atwhouser = MyUser.objects.get(username = item)
				test = "@<a href='" +'/user/'+str(atwhouser.id)+'/informations/'+"'>"+atwhouser.username+"</a>"+' '
				text = text.replace('@'+item+' ', test);
			cachekey = "comment_user_count_" + str(user.id)
			if cache.get(cachekey) != None:
				cache.incr(cachekey)
			else:
				usercomnum = Comment.objects.filter(user = user).count()
				cache.set(cachekey,  usercomnum)
			data = {
			"user": user.username,
			"text": text,
			"parentcommentext": c.parent.text,
			"parentcommentuser": str(c.parent.user),
			"commentid":c.id,
			}
			json_data = json.dumps(data)
			return HttpResponse(json_data, content_type='application/json')
		except:
			traceback.print_exc()
			raise Http404(traceback)

	else:
		raise Http404


#显示更多评论按钮
def morecomment(request):
	try:
		articleid = request.POST.get('articleid')
		article = Article.objects.get(pk=articleid)
		comment = Comment.objects.filter(article=article)
	except Article.DoesNotExist:
		raise Http404("Article does not exist")
	if request.is_ajax():
		request.session['commentlen'] = request.POST.get('commentlen')
	if comment.count() == int(request.session['commentlen']):
		loadcompleted = '已全部加载完成'
	else:
		loadcompleted = '点击加载更多'
	data = {
		'loadcompleted' : loadcompleted
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')

#收藏按钮
def collection(request):
	try:
		articleid = request.POST.get('articleid')
		article = Article.objects.get(pk=articleid)
		user = request.user
	except Article.DoesNotExist:
		raise Http404("Article does not exist")
	try:
		collection = Collection.objects.get(article=article, user=user)
	except:
		collection = None
	if collection: 
		collection.delete()
		collcount = -1
		cachekey = "article_collection_" + str(articleid)
		if cache.get(cachekey) != None:
			cache.decr(cachekey)
		else:
			cache.set(cachekey, article.collection_set.count(), settings.CACHE_EXPIRETIME)
		collecicon = '收藏'
	else:
		c = Collection(user=user, article=article)
		c.save()
		collcount = 1
		cachekey = "article_collection_" + str(articleid)
		if cache.get(cachekey) != None:
			cache.incr(cachekey)
		else:
			cache.set(cachekey, article.collection_set.count(), settings.CACHE_EXPIRETIME)
		collecicon = '已收藏'
	data = {
	 'collecicon': collecicon,
	 'collcount': collcount,
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')

#给评论点赞
def commentlike(request):
	try:
		commentid = request.POST.get('commentid')
		comment = Comment.objects.get(pk=commentid)
		user = request.user
	except Article.DoesNotExist:
		raise Http404("Article does not exist")
	try:
		commentlike = CommentLike.objects.get(comment=comment, user=user)
	except:
		commentlike = None
	if commentlike: 
		commentlikecount = -1
		#commentlike.delete()
		instancedelete.delay(commentlike)
		#减去缓存中评论点赞数
		cachekey = "comment_like_count_" + str(comment.id)
		if cache.get(cachekey) != None:
			cache.decr(cachekey)
		else:
			cache.set(cachekey,  comment.commentlike_set.count())
			cache.decr(cachekey)
		# comment.readers = comment.readers - 1
		# comment.save()
		readersout.delay(comment)
		if comment.user != user:
			commentzanminus.delay(user, comment.user, comment)
		else:
			pass
	else:
		commentlikecount = +1
		#加上缓存中评论点赞数
		cachekey = "comment_like_count_" + str(comment.id)
		if cache.get(cachekey) != None:
			cache.incr(cachekey)
		else:
			cache.set(cachekey,  comment.commentlike_set.count())
			cache.incr(cachekey)
		# comment.readers = comment.readers + 1
		# comment.save()
		readersin.delay(comment)
		c = CommentLike(user=user, comment=comment)
		#.save()
		instancesave.delay(c)
		if comment.user != user:
			commentzanplus.delay(user, comment.user, comment)
		else:
			pass
	data = {
	 'commentlikecount': commentlikecount,
	}
	json_data = json.dumps(data)
	print 'commentlike'
	return HttpResponse(json_data, content_type='application/json')

#给评论点衰
def commentdislike(request):
	try:
		commentid = request.POST.get('commentid')
		comment = Comment.objects.get(pk=commentid)
		user = request.user
	except Article.DoesNotExist:
		raise Http404("Article does not exist")
	try:
		commentdislike = CommentDisLike.objects.get(comment=comment, user=user)
	except:
		commentdislike = None
	if commentdislike: 
		commentdislikecount = -1
		#commentdislike.delete()
		instancedelete.delay(commentdislike)
		#减去缓存中评论点赞数
		cachekey = "comment_dislike_count_" + str(comment.id)
		if cache.get(cachekey) != None:
			cache.decr(cachekey)
		else:
			cache.set(cachekey,  comment.commentdislike_set.count())
			cache.decr(cachekey)
		# comment.readers = comment.readers - 1
		# comment.save()
		readersout.delay(comment)
	else:
		commentdislikecount = +1
		#加上缓存中评论点赞数
		cachekey = "comment_dislike_count_" + str(comment.id)
		if cache.get(cachekey) != None:
			cache.incr(cachekey)
		else:
			cache.set(cachekey,  comment.commentdislike_set.count())
			cache.incr(cachekey)
		# comment.readers = comment.readers + 1
		# comment.save()
		readersin.delay(comment)
		c = CommentDisLike(user=user, comment=comment)
		#c.save()
		instancesave.delay(c)
	data = {
	 'commentdislikecount': commentdislikecount,
	}
	json_data = json.dumps(data)
	#print 'commentlike'
	return HttpResponse(json_data, content_type='application/json')

#加载更多评论的页面
def commentpage(request, article_id):
	try:
		article = Article.objects.get(pk=article_id)
		comment = Comment.objects.filter(article=article)
	except Article.DoesNotExist:
		raise Http404("Article does not exist")
	if request.session.get('commentlen', False):
		commentlen = request.session['commentlen']
	commentlen = int(commentlen)
	comment = comment[commentlen:commentlen+5]
	context = {
		"comment": comment,
	}
	return render(request, 'commentpage.html',  context)

#分类文章页，加载更多文章按钮
def morearticleincat(request):
	if request.is_ajax():
		request.session['articlelen'] = request.POST.get('articlelen')
		articlelen = int(request.session['articlelen'])
		request.session['categorytitle'] = request.POST.get('categorytitle')
		categorytitle = request.session['categorytitle']
		category = Category.objects.get(title = categorytitle)
		articlequery = Relation.objects.filter(category=category).order_by('-article_id')
	if articlequery.count() == articlelen:
		loadcompleted = '已全部加载完成'
	else:
		loadcompleted = '加载更多'
		#print request.session['articlelen']
		#print request.session['categorytitle']
	data = {
		"loadcompleted": loadcompleted,
	}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


#分类文章页，加载更多文章页面
def articlepage(request):
	if request.session.get('articlelen', False):
		articlelen = request.session['articlelen']
	if request.session.get('categorytitle', False):
		categorytitle = request.session['categorytitle']
		category = Category.objects.get(title = categorytitle)
		articlequery = Relation.objects.filter(category=category).order_by('-article_id')
	articlelen = int(articlelen)
	articlequery = articlequery[articlelen:articlelen+5]
	context = {
		"articlequery": articlequery,
	}
	return render(request, 'articlepage.html',  context)

#投稿页面
def article_post(request):
	return render(request, 'article_post.html')

#实验用
from itertools import chain
def test(request):
	x = [3,2,1,4,5]
	test = []
	hotnews = Article.objects.filter(timestamp__gte=datetime.date.today() - timedelta(days=150))
	for item in x:
		# test1 = hotnews.id = get(id = item)
		for item1 in hotnews:
			if item1.id == item:
				#item1
				test.append(item1)

		#test.append(test1)
	context = {
		'test':test,
		}
	return render(request, 'test.html', context)

# def orderbyreaders(readerslist, queryset):
# 	for item in readerslist:
# 		for item1 in queryset:
# 			if item1.id == item:
# 				test.append(item1)
# 	return test


