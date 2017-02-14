# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0019_groupmanager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=DjangoUeditor.models.UEditorField(max_length=10000),
        ),
    ]
