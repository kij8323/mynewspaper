#from celery import task
#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#celery消息队列注册的函数
#注册的函数必须放在名为tasks.py的文件中
from celery.decorators import task
from accounts.models import thidauth2, thidauth1, thidauth3
import scorebill

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
    if thidauth2(x, y):
        y.score = y.score + 5
        y.save()
        sb = scorebill.models.Scorebill(user = y, score = 5, plus = True, way = 1, topic = z)
        sb.save()
        return 'success'
    else:
        pass
    return 'fail'

#验证文章作者以及点赞人是否第三方认证并判断减分
@task
def topiczanminus(x, y, z):
    if thidauth2(x, y):
        y.score = y.score - 5
        y.save()
        sb = scorebill.models.Scorebill(user = y, score = 5, plus = False, way = 2, topic = z)
        sb.save()
        return 'success'
    else:
        pass
    return 'fail'


#验证评论作者以及点赞人是否第三方认证并判断加分
@task
def commentzanplus(x, y, z):
    try:
        if thidauth2(x, y):
            y.score = y.score + 5
            y.save()
            sb = scorebill.models.Scorebill(user = y, score = 5, plus = True, way = 3, comment = z)
            sb.save()
            return 'success'
        else:
            pass
    except:
        pass
    return 'fail'

#验证评论作者以及点赞人是否第三方认证并判断减分
@task
def commentzanminus(x, y, z):
    try:
        if thidauth2(x, y):
            y.score = y.score - 5
            y.save()
            sb = scorebill.models.Scorebill(user = y, score = 5, plus = False, way = 4, comment = z)
            sb.save()
            return 'success'
        else:
            pass
    except:
        pass
    return 'fail'



#验证话题作者是否第三方验证，并判断加分
@task
def topicwritescore(x, y, z):
    try:
        if y.score == True:
            if thidauth1(x):
                x.score = x.score +150 
                x.save()
                z = z(user=x, topic=y)
                z.save()
                sb = scorebill.models.Scorebill(user = x, score = 150, plus = True, way = 5, topic = y)
                sb.save()
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
                y.score = y.score + 10
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







#申请试用加积分
@task
def prodapplscore(x):
    try:
        if thidauth1(x):
            x.score = x.score + 10
            x.save()
            return 'success'
        else:
            pass
    except:
        pass
    return 'fail'


#打卡加积分
@task
def dakascore(x):
    try:
        if thidauth1(x):
            x.score = x.score + 5 
            x.save()
            sb = scorebill.models.Scorebill(user = x, score = 5, plus = True, way = 7)
            sb.save()  
            return 'success'
        else:
            pass
    except:
        pass
    return 'fail'


#最佳评论加积分
@task
def commentscore(x, y):
    try:
        if thidauth1(x):
            x.score = x.score + 30
            x.save()
            sb = scorebill.models.Scorebill(user = x, score = 30, plus = True, way = 6, comment = y)
            sb.save()   
            return 'success'
        else:
            pass
    except:
        pass
    return 'fail'

#积分竞拍减积分
@task
def payscrerec(a,b,c,d,e):
    try:
        userpay = a.objects.filter(user=b, products=c).order_by('-payscore')
        if userpay.count() != 0:
            b.score = b.score+userpay[0].payscore-d
            b.save()
            sb = scorebill.models.Scorebill(user = b, score = d - userpay[0].payscore, plus = False, way = 8, products = c)
            sb.save()  
        else:
            b.score = b.score-d
            b.save()
            sb = scorebill.models.Scorebill(user = b, score = d, plus = False, way = 8, products = c)
            sb.save() 

        try:
            userecpay = e.objects.get(user=b, products=c)
            userecpay.payscore = d
            userecpay.save()
        except:
            p = e(user=b, products=c, payscore=d)
            p.save()
        return 'success'
    except:
        pass
    return 'fail'




#评论人是否第三方认证，判断加分
@task
def instrumentcommentplus(x, y, z):
    try:
        if thidauth1(x):
            x.score = x.score + 20
            x.save()
            z = z(user=x, instrument=y)
            z.save()  
            return 'success'
        else:
            pass
    except:
        pass
    return 'fail'
