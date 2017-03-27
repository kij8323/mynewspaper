# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0033_auto_20170304_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='img1',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
