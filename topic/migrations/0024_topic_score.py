# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0023_topic_original'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='score',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
