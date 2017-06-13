#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Comment
from django.http import Http404
from article.form import CommentForm
from judgement.models import Instrument, Category, Instrumentusercomment, Instrumentgrade

#分类文章页面
def commentdetail(request, comment_id):
	try:
		comment = Comment.objects.get(pk=comment_id)
		if comment.parent:
			comment = comment.parent
		else:
			pass
	except:
		raise Http404("Category does not exist")
	context = {
		'comment': comment,
		"form": CommentForm,
	}
	return render(request, 'commentdetail.html',  context)




def commentdetailinstrument(request, comment_id):
	try:
		comment = Comment.objects.get(pk=comment_id)
		if comment.parent:
			comment = comment.parent
		else:
			pass
	except:
		raise Http404("Category does not exist")
	instrument = comment.instrument
	try:
		instrumentgrade = Instrumentgrade.objects.get(instrument=instrument)
	except:
		instrumentgrade = Instrumentgrade()
		instrumentgrade.instrument = instrument
		instrumentgrade.save()
	context = {
		'instrument': instrument,
		'user': request.user,
		"form": CommentForm,
		"comment": comment,
		"instrumentgrade": instrumentgrade,
	}
	return render(request, 'commentdetailinstrument.html',  context)

