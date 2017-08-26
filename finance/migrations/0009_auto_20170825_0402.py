# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0008_auto_20170622_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='finance',
            name='refund',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='finance',
            name='way',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
