# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0021_auto_20161107_0217'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='savetext',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
