# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0020_comment_instrument'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='score',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
