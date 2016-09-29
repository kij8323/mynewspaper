# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0033_article_deep'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='wechat',
            field=models.BooleanField(default=False),
        ),
    ]
