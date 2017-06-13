# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='finance',
            name='testchar',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
    ]
