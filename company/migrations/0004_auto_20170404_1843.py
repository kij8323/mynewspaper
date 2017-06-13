# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_collectioncompany'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='associatetitle',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='client',
            field=ckeditor.fields.RichTextField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='industry',
            field=models.CharField(db_index=True, max_length=120, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='location',
            field=models.CharField(db_index=True, max_length=120, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='product',
            field=ckeditor.fields.RichTextField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='weburl',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
    ]
