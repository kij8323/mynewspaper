# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0042_auto_20170711_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='videotime',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
