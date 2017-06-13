# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topic', '0038_auto_20170326_2105'),
        ('products', '0017_payscorerec'),
        ('comment', '0021_comment_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scorebill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('plus', models.BooleanField(default=True)),
                ('way', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('comment', models.ForeignKey(blank=True, to='comment.Comment', null=True)),
                ('products', models.ForeignKey(blank=True, to='products.Products', null=True)),
                ('topic', models.ForeignKey(blank=True, to='topic.Topic', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
