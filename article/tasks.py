#from celery import task
#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#celery消息队列注册的函数
#注册的函数必须放在名为tasks.py的文件中
from celery.decorators import task
from accounts.models import thidauth2, thidauth1, thidauth3

#更新数据库readers+1
@task
def readersin(x):
    x.readers+= 1
    x.save()
    return 'readers +1 success!'

#更新数据库readers-1
@task
def readersout(x):
    x.readers-= 1
    x.save()
    return 'readers -1 success!'

#删除数据库中数据
@task
def instancedelete(x):
    x.delete()
    return 'delete success!'

#向数据库中写入数据
@task
def instancesave(x):
    x.save()
    return 'save success!'

#做实验用的函数
@task
def add(x, y):
  return x + y



#验证文章作者以及点赞人是否第三方认证并判断加分
@task
def topiczanplus(x, y, z):
    if z.score == True:
        if thidauth2(x, y):
            y.score = y.score + 5
            y.save()
        else:
            pass
    else:
        pass
    return 'score success!'

#验证文章作者以及点赞人是否第三方认证并判断减分
@task
def topiczanminus(x, y, z):
    if z.score == True:
        if thidauth2(x, y):
            y.score = y.score - 5
            y.save()
        else:
            pass
    else:
        pass
    return 'score success!'



#验证评论作者以及点赞人是否第三方认证并判断加分
@task
def commentzanplus(x, y, z):
    try:
        if z.topic.score == True:
            if thidauth2(x, y):
                y.score = y.score + 5
                y.save()
            else:
                pass
        else:
            pass
    except:
        pass
    return 'score success!'

#验证评论作者以及点赞人是否第三方认证并判断减分
@task
def commentzanminus(x, y, z):
    try:
        if z.topic.score == True:
            if thidauth2(x, y):
                y.score = y.score - 5
                y.save()
            else:
                pass
        else:
            pass
    except:
        pass
    return 'score success!'


#验证话题作者是否第三方验证，并判断加分
@task
def topicwritescore(x, y, z):
    try:
        if y.score == True:
            if thidauth1(x):
                x.score = x.score + 20
                x.save()
                z = z(user=x, topic=y)
                z.save()
            else:
                pass
        else:
            pass
    except:
        pass
    return 'score success!'



#验证文章作者和评论人是否第三方认证，判断加分
@task
def topiccommentplus(x, y, z, a):
    try:
        if z.score == True:
            if thidauth2(x, y):
                y.score = y.score + 20
                y.save()
                x.score = x.score + 10
                x.save()
                a = a(user=y, topic=z)
                a.save()    
            else:
                pass
        else:
            pass
    except:
        pass
    return 'score success!'



#作者回复他人评论时，作者加10分是否第三方认证，判断加分
@task
def topicwritereplyplus(x, y, z, a):
    try:
        if z.score == True:
            if thidauth2(x, y):
                x.score = x.score + 10
                x.save()
                a = a(user=y, topic=z)
                a.save()    
            else:
                pass
        else:
            pass
    except:
        pass
    return 'score success!'




#评论获他人回复,是否第三方认证，判断加分
@task
def topiccommentreplyplus(x, y, z, a, b):
    try:
        if a.score == True:
            if thidauth3(x, y, z):
                x.score = x.score + 10
                x.save()
                y.score = y.score + 10
                y.save()                         
                b = b(user1=z, user2=y, topic=a)
                b.save()    
            else:
                pass
        else:
            pass
    except:
        pass
    return 'score success!'
