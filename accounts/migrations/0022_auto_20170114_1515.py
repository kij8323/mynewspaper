# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_weixinuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weibouser',
            name='logpassword',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='weixinuser',
            name='logpassword',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
    ]
