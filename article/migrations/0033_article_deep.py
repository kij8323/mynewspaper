# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0032_article_investment'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='deep',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
