# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_auto_20170612_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='oneresult',
            field=DjangoUeditor.models.UEditorField(max_length=10000, null=True, blank=True),
        ),
    ]
