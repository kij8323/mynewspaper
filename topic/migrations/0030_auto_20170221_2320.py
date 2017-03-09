# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0029_topic_guanggao'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='imagefst3',
            field=models.ImageField(null=True, upload_to=b'images/', blank=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='imagescd3',
            field=models.ImageField(null=True, upload_to=b'images/', blank=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='imagethd3',
            field=models.ImageField(null=True, upload_to=b'images/', blank=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='img3',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
