# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0041_auto_20170711_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=DjangoUeditor.models.UEditorField(max_length=150000, null=True, blank=True),
        ),
    ]
