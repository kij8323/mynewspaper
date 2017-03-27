# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0018_comment_products'),
        ('topic', '0035_daka'),
        ('products', '0017_payscorerec'),
    ]

    operations = [
        migrations.CreateModel(
            name='Updatenew',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('comment', models.ForeignKey(blank=True, to='comment.Comment', null=True)),
                ('payscore', models.ForeignKey(blank=True, to='products.Payscore', null=True)),
                ('topic', models.ForeignKey(blank=True, to='topic.Topic', null=True)),
            ],
        ),
    ]
