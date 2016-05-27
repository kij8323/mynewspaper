# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0029_auto_20160503_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='original',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=20000, null=True, blank=True),
        ),
    ]
