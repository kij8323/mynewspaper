# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0016_topic_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='images1',
            field=models.ImageField(null=True, upload_to=b'images/', blank=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='images2',
            field=models.ImageField(null=True, upload_to=b'images/', blank=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='images3',
            field=models.ImageField(null=True, upload_to=b'images/', blank=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='images4',
            field=models.ImageField(null=True, upload_to=b'images/', blank=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='images5',
            field=models.ImageField(null=True, upload_to=b'images/', blank=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='images6',
            field=models.ImageField(null=True, upload_to=b'images/', blank=True),
        ),
    ]
