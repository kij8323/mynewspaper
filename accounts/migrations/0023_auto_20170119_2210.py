# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20170114_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='qianming',
            field=models.CharField(default=b'\xe8\xbf\x99\xe5\xae\xb6\xe4\xbc\x99\xe7\x9c\x9f\xe5\xbf\x83\xe6\x87\x92\xef\xbc\x8c\xe4\xbb\x80\xe4\xb9\x88\xe9\x83\xbd\xe6\xb2\xa1\xe5\x86\x99.', max_length=200),
        ),
        migrations.AddField(
            model_name='myuser',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='weibouser',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='weixinuser',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
