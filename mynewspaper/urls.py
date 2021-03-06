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

    url(r'^home/moretopichome/$', 'mainpage.views.moretopichome', name='moretopichome'),#首页更多文章按钮ajax

    url(r'^home/topicpagehome/$', 'mainpage.views.topicpagehome', name='topicpagehome'),#首页更多文章加载页面

    url(r'^home/articlepagehome/$', 'mainpage.views.articlepagehome', name='articlepagehome'),#首页更多文章加载页面
    url(r'^home/index_search/$', 'mainpage.views.index_search', name='index_search'),#搜索页面

    url(r'^homepage/$', 'mainpage.views.homepage', name='homepage'),#首页加载



    url(r'^home/morearticlexshome/$', 'mainpage.views.morearticlexshome', name='morearticlexshome'),#首页更多文章按钮ajax
    url(r'^home/articlepagexshome/$', 'mainpage.views.articlepagexshome', name='articlepagexshome'),#首页更多文章加载页面


    url(r'^home/products-list-xs-page/$', 'mainpage.views.homeproductslistxspage', name='homeproductslistxspage'),#搜索页面
    url(r'^home/products-list-lg-page/$', 'mainpage.views.homeproductslistlgpage', name='homeproductslistlgpage'),#搜索页面

    url(r'^home/topic-list-xs-page/$', 'mainpage.views.hometopiclistxspage', name='hometopiclistxspage'),#搜索页面
    url(r'^home/topic-list-lg-page/$', 'mainpage.views.hometopiclistlgpage', name='hometopiclistlgpage'),#搜索页面

    url(r'^home/comment-list-xs-page/$', 'mainpage.views.homecommentlistxspage', name='homecommentlistxspage'),#搜索页面
    url(r'^home/comment-list-lg-page/$', 'mainpage.views.homecommentlistlgpage', name='homecommentlistlgpage'),#搜索页面

    url(r'^home/update-list-xs-page/$', 'mainpage.views.homeupdatelistxspage', name='homeupdatelistxspage'),#搜索页面
    url(r'^home/update-list-lg-page/$', 'mainpage.views.homeupdatelistlgpage', name='homeupdatelistlgpage'),#搜索页面

    url(r'^home/rules-list-xs-page/$', 'mainpage.views.homeruleslistxspage', name='homeruleslistxspage'),#搜索页面
    url(r'^home/rules-list-lg-page/$', 'mainpage.views.homeruleslistlgpage', name='homeruleslistlgpage'),#搜索页面


    url(r'^home/discovery-list-lg-page/$', 'mainpage.views.homediscoverylistlgpage', name='homediscoverylistlgpage'),#搜索页面

    url(r'^home/discovery-list-xs-page/$', 'mainpage.views.homediscoverylistxspage', name='homediscoverylistxspage'),#搜索页面




    url(r'^user/(?P<user_id>[0-9]+)/thirdfirstloggin', 'accounts.views.thirdfirstloggin', name='thirdfirstloggin'),

    url(r'^user/weixin/disconnection', 'accounts.views.disweixinconnection', name='disweixinconnection'),#已有帐号者的微信链接
    url(r'^user/weibo/disconnection', 'accounts.views.disweiboconnection', name='disweiboconnection'),#已有帐号者的微信链接
    url(r'^user/weibo/connection', 'accounts.views.weiboconnection', name='weiboconnection'),#已有帐号者的微信链接
    url(r'^user/weixin/connection', 'accounts.views.weixinconnection', name='weixinconnection'),#已有帐号者的微信链接
    url(r'^user/loggin/weixin', 'accounts.views.logginweixin', name='logginweixin'),#登录wexin
    url(r'^user/loggin/third', 'accounts.views.logginthird', name='logginthird'),#登录webo
    url(r'^user/loggin/weibo', 'accounts.views.logginweibo', name='logginweibo'),#登录webo
    url(r'^user/loggin/', 'accounts.views.loggin', name='loggin'),#登录
    url(r'^user/userlogout/', 'accounts.views.userlogout', name='userlogout'),#用户登出，不用
    url(r'^user/register/', 'accounts.views.register', name='register'),#用户注册
    url(r'^user/inbox/', 'accounts.views.inbox', name='inbox'),#消息数ajax  
    url(r'^user/repassword/', 'accounts.views.repassword', name='repassword'),#登录
    url(r'^captcha/', include('captcha.urls')),  #验证码设置
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),#富文本框
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
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
    url(r'^user/(?P<user_id>[0-9]+)/collectionsinvestment/$', 'accounts.views.userdashboardcollectionsinvestment', name='user_detailcollectionsinvestment'),#个人收藏话题

   url(r'^user/(?P<user_id>[0-9]+)/try/$', 'accounts.views.userdashboardtry', name='user_detailtry'),#个人试用
   url(r'^user/notificationsconversation/$', 'accounts.views.notificationsconversation', name='notificationsconversation'),#私信ajax

    url(r'^user/(?P<user_id>[0-9]+)/subscription/$', 'accounts.views.subscription', name='user_subscription'),#个人试用
    url(r'^user/dosubscription/$', 'accounts.views.dosubscription', name='dosubscription'),#个人试用


    url(r'^group/index/$', 'topic.views.group_index', name='group_index'),#不用
    url(r'^group/all/$', 'topic.views.group_all', name='group_all'),#话题组首页
    url(r'^group/(?P<group_id>[0-9]+)/$', 'topic.views.group_detail', name='group_detail'),#话题组页
    url(r'^group/(?P<group_id>[0-9]+)/score/$', 'topic.views.group_score', name='group_score'),#话题组页
    url(r'^groupall/score/$', 'topic.views.groupall_score', name='groupall_score'),#
    url(r'^groupallpage/$', 'topic.views.groupallpage', name='groupallpage'),#加载话题组页
    url(r'^groupdetailpage/$', 'topic.views.groupdetailpage', name='groupdetailpage'),#加载话题组页
    url(r'^grouplist/$', 'topic.views.grouplist', name='grouplist'),#加载话题组页


    url(r'^topiccommentpage/(?P<topic_id>[0-9]+)/$', 'topic.views.topiccommentpage', name='topiccommentpage'),#加载话题评论

    url(r'^topicdetailpage/(?P<topic_id>[0-9]+)/$', 'topic.views.topicdetailpage', name='topicdetailpage'),#话题页



    url(r'^topic/(?P<topic_id>[0-9]+)/$', 'topic.views.topic_detail', name='topic_detail'),#话题页
    url(r'^topic/newtopic/$', 'topic.views.newtopic', name='newtopic'),#新建话题页
    url(r'^topic/topicomment/$', 'topic.views.topicomment', name='topicomment'),#发表话题评论页ajax
    url(r'^topic/topcommentcomment/$', 'topic.views.topcommentcomment', name='topcommentcomment'),#发表话题评论的评论页
    #url(r'^topic/atwhoidentify/$', 'topic.views.atwhoidentify', name='atwhoidentify'),#话题页将@的用户添加链接
    url(r'^topic/moretopic/$', 'topic.views.moretopic', name='moretopic'),#话题组页，增多话题
    url(r'^topic/groupage/$', 'topic.views.groupage', name='groupage'),#话题组页，加载更多话题页面
    url(r'^topic/collectiontopic/$', 'topic.views.collectiontopic', name='collectiontopic'),#收藏话题
    url(r'^topic/renewtopic/(?P<topic_id>[0-9]+)/$', 'topic.views.renewtopic', name='renewtopic'),#编辑话题
    url(r'^topic/mobilenew/$', 'topic.views.mobilenew', name='mobilenew'),#编辑话题
    url(r'^topic/dianzan/$', 'topic.views.dianzan', name='topicdianzan'),#编辑话题
    url(r'^topic/daka/$', 'topic.views.daka', name='daka'),#编辑话题
    url(r'^topic/morecomment/$', 'topic.views.topicmorecomment', name='topicmorecomment'),#文章页显示更多评论按钮
    url(r'^topic/morecommentpage/(?P<topic_id>[0-9]+)/$', 'topic.views.topicmorecommentpage', name='topicmorecommentpage'),#文章页加载更多评论页面



    url(r'^articlecomment/$', 'article.views.articlecomment', name='articlecomment'),#文章评论
    url(r'^commentcomment/$', 'article.views.commentcomment', name='commentcomment'),#文章评论的评论
    url(r'^morecomment/$', 'article.views.morecomment', name='morecomment'),#文章页显示更多评论按钮
    url(r'^category/(?P<category_id>[0-9]+)/$', 'article.views.category_detail', name='category_detail'),#文章分类页
    url(r'^category/morearticleincat/$', 'article.views.morearticleincat', name='morearticleincat'),#文章分类页，更多文章按钮
    url(r'^category/articlepage/$', 'article.views.articlepage', name='articlepage'),#文章分类页，加载更多文章页面
    url(r'^category/all/$', 'article.views.category_all', name='category_all'),#所有文章页


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


   url(r'^investment/list/id/$', 'investment.views.investment_list_id', name='investment_list_id'),#公司页
    url(r'^investment/list/index/$', 'investment.views.investment_list_index', name='investment_list_index'),#公司页
    url(r'^investment/(?P<investment_id>[0-9]+)/$', 'investment.views.investment_detail', name='investment_detail'),#公司页
    url(r'^topic/collectioninvestment/$', 'investment.views.collectioninvestment', name='collectioninvestment'),#收藏公司
    url(r'^investment/built/$', 'investment.views.investmentbuilt', name='investmentbuilt'),#收藏公司

    url(r'^productsallpage/$', 'products.views.productsallpage', name='productsallpage'),#试用首页加载

   url(r'^products/all/$', 'products.views.productsall', name='productsall'),#试用首页
    url(r'^products/applying/$', 'products.views.productsapplying', name='productsapplying'),#试用首页
    url(r'^products/testing/$', 'products.views.productstesting', name='productstesting'),#试用首页
    url(r'^products/finish/$', 'products.views.productsfinish', name='productsfinish'),
    url(r'^products/moreproducts/$', 'products.views.moreproducts', name='moreproducts'),
    url(r'^products/productspage/$', 'products.views.productspage', name='productspage'),
    url(r'^products/payscore/$', 'products.views.payscore', name='payscore'),
    url(r'^products/payscorerecord/(?P<products_id>[0-9]+)/$', 'products.views.payscorerecord', name='payscorerecord'),
    



    url(r'^products/(?P<products_id>[0-9]+)/$', 'products.views.products_detail', name='products_detail'),#试用页
    url(r'^productscomment/$', 'products.views.productscomment', name='productscomment'),#试用评论
    url(r'^products/productscommentcomment/$', 'products.views.productscommentcomment', name='productscommentcomment'),#发表话题评论的评论
    url(r'^products/morecomment/$', 'products.views.productsmorecomment', name='productsmorecomment'),#文章页显示更多评论按钮
    url(r'^products/commentpage/(?P<products_id>[0-9]+)/$', 'products.views.productscommentpage', name='productscommentpage'),#文章页加载更多评论页面
   url(r'^products/apply/(?P<products_id>[0-9]+)/$', 'products.views.productsapply', name='productsapply'),#文章页加载更多评论页面
    url(r'^products/report/(?P<products_id>[0-9]+)/$', 'products.views.productsreport', name='productsreport'),

    url(r'^products/test123xxxnewapplication/(?P<products_id>[0-9]+)/(?P<app_num>[0-9]+)/(?P<period_num>[0-9]+)/$', 'products.views.newapplication', name='newapplication'),#对id为4的产品，生成4个机器人申请，每100秒一个
    url(r'^products/test123xxxfunction/$', 'products.views.function', name='function'),
    url(r'^products/one/(?P<products_id>[0-9]+)/$', 'products.views.productsone', name='productsone'),#文章页加载更多评论页面



    url(r'^comment/(?P<comment_id>[0-9]+)/$', 'comment.views.commentdetail', name='commentdetail'),#个人信息
    url(r'^comment/instrument/(?P<comment_id>[0-9]+)/$', 'comment.views.commentdetailinstrument', name='commentdetailinstrument'),#个人信息


    url(r'^judgement/$', 'judgement.views.judgement', name='judgement'),#评分页
    url(r'^instrument/(?P<instrument_id>[0-9]+)/$', 'judgement.views.instrumentdetail', name='instrument_detail'),#评分页

    url(r'^instrumentpage/(?P<category_id>[0-9]+)/$', 'judgement.views.instrumentpage', name='instrumentpage'),#

    url(r'^instrument/moreinstru/$', 'judgement.views.moreinstru', name='moreinstru'),
    url(r'^instrument/moreinstrupage/$', 'judgement.views.moreinstrupage', name='moreinstrupage'),
    url(r'^instrument/instrumentcomment/$', 'judgement.views.instrumentcomment', name='instrumentcomment'),#发表话题评论页ajax
    url(r'^instrument/instrucommentcomment/$', 'judgement.views.instrucommentcomment', name='instrucommentcomment'),#发表话题评论页ajax

    url(r'^instrument/index/$', 'judgement.views.instrumentindex', name='instrumentindex'),#发表话题评论页ajax
    url(r'^newinstru/$', 'judgement.views.newinstru', name='newinstru'),#

    url(r'^scorebillpage/(?P<user_id>[0-9]+)/$', 'scorebill.views.scorebillpage', name='scorebillpage'),#搜索页面

    url(r'^scorerankpage/$', 'scorebill.views.scorerankpage', name='scorerankpage'),#搜索页面
 
    url(r'^onebillpage/(?P<user_id>[0-9]+)/$', 'finance.views.onebillpage', name='onebillpage'),#搜索页面

    url(r'^weixin/financegz/$', 'finance.views.weixinfinancegz', name='weixinfinancegz'),#
 


    url(r'^weixin/finance/$', 'finance.views.weixinfinance', name='weixinfinance'),#
    url(r'^alipay/finance/$', 'finance.views.alipayfinance', name='alipayfinance'),#
    url(r'^alipay/redirect/finance/$', 'finance.views.alipayredirectfinance', name='alipayredirectfinance'),#
    url(r'^alipay/notify/finance/$', 'finance.views.alipaynotifyfinance', name='alipaynotifyfinance'),#
    url(r'^alipay/gateway/finance/$', 'finance.views.alipaygatewayfinance', name='alipaygatewayfinance'),#
    url(r'^weixin/notify/finance/$', 'finance.views.weixinnotifyfinance', name='weixingnotifyfinance'),#


    url(r'^alipay/refund/finance/$', 'finance.views.alipayrefundfinance', name='alipayrefundfinance'),#
    url(r'^weixin/refund/finance/$', 'finance.views.weixinrefundfinance', name='weixinrefundfinance'),#


    url(r'^discovery/updatediscoverytaihuoniao/$', 'discovery.views.updatediscoverytaihuoniao', name='updatediscoverytaihuoniao'),#
    url(r'^discovery/discoverytaihuoniao/$', 'discovery.views.discoverytaihuoniao', name='discoverytaihuoniao'),#


    url(r'^discovery/updatediscoverysmzdm/$', 'discovery.views.updatediscoverysmzdm', name='updatediscoverysmzdm'),#
    url(r'^discovery/discoverysmzdm/$', 'discovery.views.discoverysmzdm', name='discoverysmzdm'),#



    url(r'^discovery/updatediscoverytengxuncar/$', 'discovery.views.updatediscoverytengxuncar', name='updatediscoverytengxuncar'),#
    url(r'^discovery/discoverytengxuncar/$', 'discovery.views.discoverytengxuncar', name='discoverytengxuncar'),#



    url(r'^discovery/updatediscoveryjuyoufan/$', 'discovery.views.updatediscoveryjuyoufan', name='updatediscoveryjuyoufano'),#
    url(r'^discovery/discoveryjuyoufan/$', 'discovery.views.discoveryjuyoufan', name='discoveryjuyoufan'),#



    url(r'^discovery/updatediscoveryairanshao/$', 'discovery.views.updatediscoveryairanshao', name='updatediscoveryairanshao'),#
    url(r'^discovery/discoveryairanshao/$', 'discovery.views.discoveryairanshao', name='discoveryairanshao'),#



    url(r'^discovery/updatediscoveryzol/$', 'discovery.views.updatediscoveryzol', name='updatediscoveryzol'),#
    url(r'^discovery/discoveryzol/$', 'discovery.views.discoveryzol', name='discoveryzol'),#


    url(r'^discovery/updatediscoveryzhiyou/$', 'discovery.views.updatediscoveryzhiyou', name='updatediscoveryzhiyou'),#
    url(r'^discovery/discoveryzhiyou/$', 'discovery.views.discoveryzhiyou', name='discoveryzhiyou'),#



    url(r'^discovery/updatediscoverywaishetianxia/$', 'discovery.views.updatediscoverywaishetianxia', name='updatediscoverywaishetianxia'),#
    url(r'^discovery/discoverywaishetianxia/$', 'discovery.views.discoverywaishetianxia', name='discoverywaishetianxia'),#


    url(r'^discovery/updatediscoveryzhinengjie/$', 'discovery.views.updatediscoveryzhinengjie', name='updatediscoveryzhinengjie'),#
    url(r'^discovery/discoveryzhinengjie/$', 'discovery.views.discoveryzhinengjie', name='discoveryzhinengjie'),#



    url(r'^discovery/updatediscoveryyewan/$', 'discovery.views.updatediscoveryyewan', name='updatediscoveryyewan'),#
    url(r'^discovery/discoveryyewan/$', 'discovery.views.discoveryyewan', name='discoveryyewan'),#



    url(r'^discovery/updatediscoverytaipingyang/$', 'discovery.views.updatediscoverytaipingyang', name='updatediscoverytaipingyang'),#
    url(r'^discovery/discoverytaipingyang/$', 'discovery.views.discoverytaipingyang', name='discoverytaipingyang'),#




    url(r'^discovery/updatediscoveryzhinengbang/$', 'discovery.views.updatediscoveryzhinengbang', name='updatediscoveryzhinengbang'),#
    url(r'^discovery/discoveryzhinengbang/$', 'discovery.views.discoveryzhinengbang', name='discoveryzhinengbang'),#


    url(r'^discovery/updatediscoveryjingdong/$', 'discovery.views.updatediscoveryjingdong', name='updatediscoveryjingdong'),#
    url(r'^discovery/discoveryjingdong/$', 'discovery.views.discoveryjingdong', name='discoveryjingdong'),#


    url(r'^discovery/updatediscoveryit168/$', 'discovery.views.updatediscoveryit168', name='updatediscoveryit168'),#
    url(r'^discovery/discoveryit168/$', 'discovery.views.discoveryit168', name='discoveryit168'),#



    url(r'^discovery/updatediscoveryznds/$', 'discovery.views.updatediscoveryznds', name='updatediscoveryznds'),#
    url(r'^discovery/discoveryznds/$', 'discovery.views.discoveryznds', name='discoveryznds'),#


    url(r'^discovery/updatediscoverygaoqing/$', 'discovery.views.updatediscoverygaoqing', name='updatediscoverygaoqing'),#
    url(r'^discovery/discoverygaoqing/$', 'discovery.views.discoverygaoqing', name='discoverygaoqing'),#



    url(r'^discovery/updatediscoverysina/$', 'discovery.views.updatediscoverysina', name='updatediscoverysina'),#
    url(r'^discovery/discoverysina/$', 'discovery.views.discoverysina', name='discoverysina'),#


    url(r'^discovery/updatediscoverymogu/$', 'discovery.views.updatediscoverymogu', name='updatediscoverymogu'),#
    url(r'^discovery/discoverymogu/$', 'discovery.views.discoverymogu', name='discoverymogu'),#



    url(r'^discovery/updatediscoverygaoji/$', 'discovery.views.updatediscoverygaoji', name='updatediscoverygaoji'),#
    url(r'^discovery/discoverygaoji/$', 'discovery.views.discoverygaoji', name='discoverygaoji'),#

    url(r'^discovery/updatediscoveryjiguo/$', 'discovery.views.updatediscoveryjiguo', name='updatediscoveryjiguo'),#
    url(r'^discovery/discoveryjiguo/$', 'discovery.views.discoveryjiguo', name='discoveryjiguo'),#
    url(r'^discovery/$', 'discovery.views.discovery', name='discovery'),#
    url(r'^discoverypage/$', 'discovery.views.discoverypage', name='discoverypage'),#试用首页加载
    url(r'^discovery/morediscovery/$', 'discovery.views.morediscovery', name='morediscovery'),


    url(r'^discovery/(?P<category_id>[0-9]+)/$', 'discovery.views.discoverycategory', name='discoverycategory'),#
    url(r'^discoverypage/category/$', 'discovery.views.discoverycategorypage', name='discoverycategorypage'),#试用首页加载
    url(r'^discovery/morediscovery/category/$', 'discovery.views.morediscoverycategory', name='morediscoverycategory'),

    url(r'^discovery/strart/$', 'discovery.views.discoverystrart', name='discoverystrart'),



#    url(r'^products/address/(?P<products_id>[0-9]+)/$', 'products.views.productsaddress', name='productsaddress'),#文章页加载更多评论页面
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
