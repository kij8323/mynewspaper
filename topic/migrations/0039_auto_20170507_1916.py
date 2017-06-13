# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0038_auto_20170326_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='imagesugg',
            field=models.ImageField(null=True, upload_to=b'images/topic/', blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='image',
            field=models.ImageField(null=True, upload_to=b'images/topic/', blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='imagefst3',
            field=models.ImageField(null=True, upload_to=b'images/topic/', blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='imagescd3',
            field=models.ImageField(null=True, upload_to=b'images/topic/', blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='imagethd3',
            field=models.ImageField(null=True, upload_to=b'images/topic/', blank=True),
        ),
    ]
