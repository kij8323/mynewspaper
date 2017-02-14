# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20161207_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='introduction',
            field=DjangoUeditor.models.UEditorField(max_length=30000),
        ),
    ]
