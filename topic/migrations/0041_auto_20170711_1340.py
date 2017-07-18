# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0040_topic_associatetitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='ifvideo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='topic',
            name='videoaddr',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
