#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from .models import Topic
from django.forms import ModelForm


class TopicForm(ModelForm):
	class Meta:
		model = Topic
		fields = ['title', 'content']
   
