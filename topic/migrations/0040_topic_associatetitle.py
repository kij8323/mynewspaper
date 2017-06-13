# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0039_auto_20170507_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='associatetitle',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
    ]
