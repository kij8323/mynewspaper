# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0028_topiccommentreply'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='guanggao',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
