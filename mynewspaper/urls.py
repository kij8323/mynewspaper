#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^weixinyanzheng/', 'mainpage.views.weixinyanzheng', name='weixinyanzheng'),#微信验证
    url(r'^$', 'mainpage.views.home', name='home'),#主页
    url(r'^aboutus/', 'mainpage.views.aboutus', name='aboutus'),#关于我们
    url(r'^joinus/', 'mainpage.views.joinus', name='joinus'),#加入我们
    url(r'^contactus/', 'mainpage.views.contactus', name='contactus'),#联系我们
    url(r'^home/morearticlehome/$', 'mainpage.views.morearticlehome', name='morearticlehome'),#首页更多文章按钮ajax
    url(r'^home/articlepagehome/$', 'mainpage.views.articlepagehome', name='articlepagehome'),#首页更多文章加载页面
    url(r'^home/index_search/$', 'mainpage.views.index_search', name='index_search'),#搜索页面
    

    url(r'^user/loggin/', 'accounts.views.loggin', name='loggin'),#登录
    url(r'^user/userlogout/', 'accounts.views.userlogout', name='userlogout'),#用户登出，不用
    url(r'^user/register/', 'accounts.views.register', name='register'),#用户注册
    url(r'^user/inbox/', 'accounts.views.inbox', name='inbox'),#消息数ajax  

    url(r'^captcha/', include('captcha.urls')),  #验证码设置
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),#富文本框
    url(r'^captchaview/$', 'accounts.views.captchaview', name='captchaview'),#刷新验证码ajax
    url(r'^accountsview/$', 'accounts.views.accountsview', name='accountsview'),#ajax，验证用户名是否已被注册,post
    #用户信息页面
    url(r'^user/(?P<user_id>[0-9]+)/informations/$', 'accounts.views.userdashboardinformations', name='user_detailinformations'),#个人信息
    url(r'^user/(?P<user_id>[0-9]+)/comments/$', 'accounts.views.userdashboardcomments', name='user_detailcomments'),#个人评论
    url(r'^user/(?P<user_id>[0-9]+)/notifications/$', 'accounts.views.userdashboardnotifications', name='user_detailnotifications'),#个人消息@
    url(r'^user/(?P<user_id>[0-9]+)/privcynotifications/$', 'accounts.views.privcynotifications', name='user_privcynotifications'),#个人消息，私信
    url(r'^user/(?P<user_id>[0-9]+)/collections/$', 'accounts.views.userdashboardcollections', name='user_detailcollections'),#个人收藏文章
    url(r'^user/(?P<user_id>[0-9]+)/collectionstopic/$', 'accounts.views.userdashboardcollectionstopic', name='user_detailcollectionstopic'),#个人收藏话题
    url(r'^user/(?P<user_id>[0-9]+)/article/$', 'accounts.views.userdashboardarticle', name='user_userdashboardarticle'),#个人文章
    url(r'^user/(?P<user_id>[0-9]+)/articletopic/$', 'accounts.views.userdashboardarticletopic', name='user_userdashboardarticletopic'),#个人话题
    url(r'^user/(?P<user_id>[0-9]+)/userdashboard_commentocomment/$', 'accounts.views.userdashboard_commentocomment', name='userdashboard_commentocomment'),#个人点评
    url(r'^user/deleteinfo/$', 'accounts.views.deleteinfo', name='deleteinfo'),#删除个人收藏、评论。。。。。
    url(r'^user/(?P<user_id>[0-9]+)/company/$', 'accounts.views.userdashboardcompany', name='user_userdashboardcompany'),#个人公司
    url(r'^user/(?P<user_id>[0-9]+)/collectionscompany/$', 'accounts.views.userdashboardcollectionscompany', name='user_detailcollectionscompany'),

    url(r'^group/index/$', 'topic.views.group_index', name='group_index'),#不用
    url(r'^group/all/$', 'topic.views.group_all', name='group_all'),#话题组首页
    url(r'^group/(?P<group_id>[0-9]+)/$', 'topic.views.group_detail', name='group_detail'),#话题组页
    url(r'^topic/(?P<topic_id>[0-9]+)/$', 'topic.views.topic_detail', name='topic_detail'),#话题页
    url(r'^topic/newtopic/$', 'topic.views.newtopic', name='newtopic'),#新建话题页
    url(r'^topic/topicomment/$', 'topic.views.topicomment', name='topicomment'),#发表话题评论页ajax
    url(r'^topic/topcommentcomment/$', 'topic.views.topcommentcomment', name='topcommentcomment'),#发表话题评论的评论页
    #url(r'^topic/atwhoidentify/$', 'topic.views.atwhoidentify', name='atwhoidentify'),#话题页将@的用户添加链接
    url(r'^topic/moretopic/$', 'topic.views.moretopic', name='moretopic'),#话题组页，增多话题
    url(r'^topic/groupage/$', 'topic.views.groupage', name='groupage'),#话题组页，加载更多话题页面
    url(r'^topic/collectiontopic/$', 'topic.views.collectiontopic', name='collectiontopic'),#收藏话题


    url(r'^articlecomment/$', 'article.views.articlecomment', name='articlecomment'),#文章评论
    url(r'^commentcomment/$', 'article.views.commentcomment', name='commentcomment'),#文章评论的评论
    url(r'^morecomment/$', 'article.views.morecomment', name='morecomment'),#文章页显示更多评论按钮
    url(r'^category/(?P<category_id>[0-9]+)/$', 'article.views.category_detail', name='category_detail'),#文章分类页
    url(r'^category/morearticleincat/$', 'article.views.morearticleincat', name='morearticleincat'),#文章分类页，更多文章按钮
    url(r'^category/articlepage/$', 'article.views.articlepage', name='articlepage'),#文章分类页，加载更多文章页面

    url(r'^article/(?P<article_id>[0-9]+)/$', 'article.views.article_detail', name='article_detail'),#文章页
    url(r'^article/commentpage/(?P<article_id>[0-9]+)/$', 'article.views.commentpage', name='commentpage'),#文章页加载更多评论页面
    url(r'^article/collection/$', 'article.views.collection', name='collection'),#文章页收藏
    url(r'^article/test/$', 'article.views.test', name='test'),#实验
    url(r'^article/commentlike/$', 'article.views.commentlike', name='commentlike'),#文章页评论点赞
    url(r'^article/commentdislike/$', 'article.views.commentdislike', name='commentdislike'),#文章页评论点衰
    url(r'^article/article_post/$', 'article.views.article_post', name='article_post'),#首页投稿

    url(r'^company/(?P<company_id>[0-9]+)/$', 'company.views.company_detail', name='company_detail'),#公司页
    url(r'^company/list/$', 'company.views.company_list', name='company_list'),#公司页
    url(r'^company/list-fresh/$', 'company.views.company_list_fresh', name='company_list_fresh'),#公司页
    url(r'^company/content-fresh/$', 'company.views.company_content_fresh', name='company_content_fresh'),#公司页
    url(r'^company/built1/$', 'company.views.company_built1', name='company_built1'),#公司页
    url(r'^company/built2/$', 'company.views.company_built2', name='company_built2'),#公司页
    url(r'^company/(?P<company_id>[0-9]+)/built3/$', 'company.views.company_built3', name='company_built3'),#公司页
    url(r'^company/builtsucss/$', 'company.views.builtsucss', name='builtsucss'),#公司success页
    url(r'^topic/collectioncompany/$', 'company.views.collectioncompany', name='collectioncompany'),#收藏公司


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
