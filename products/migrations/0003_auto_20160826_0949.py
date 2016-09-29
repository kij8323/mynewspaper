# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_application_verify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='introduction',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=20000, null=True, blank=True),
        ),
    ]
