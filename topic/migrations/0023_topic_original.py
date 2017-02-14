# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0022_topic_savetext'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='original',
            field=models.BooleanField(default=True),
        ),
    ]
