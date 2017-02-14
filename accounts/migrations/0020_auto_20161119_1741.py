# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_repassworduser_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeiboUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weiboid', models.CharField(max_length=2000)),
                ('weiboname', models.CharField(max_length=2000, null=True, blank=True)),
                ('iconaddress', models.CharField(max_length=2000, null=True, blank=True)),
                ('logpassword', models.CharField(max_length=2000)),
            ],
        ),
        migrations.AddField(
            model_name='myuser',
            name='thirdicon',
            field=models.CharField(default=None, max_length=2000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='weibouser',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
