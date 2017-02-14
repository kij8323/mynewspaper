# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20161119_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeixinUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weixinid', models.CharField(max_length=2000)),
                ('weixinname', models.CharField(max_length=2000, null=True, blank=True)),
                ('iconaddress', models.CharField(max_length=2000, null=True, blank=True)),
                ('logpassword', models.CharField(max_length=2000)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
