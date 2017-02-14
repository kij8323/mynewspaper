# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0017_auto_20161029_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=DjangoUeditor.models.UEditorField(max_length=5000),
        ),
    ]
