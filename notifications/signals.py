#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.dispatch import Signal

#注册消息
notify = Signal(providing_args=['target_object', 'verb', 'text'
								, 'target_article', 'target_topic', 'target_products', 'target_instrument'])
