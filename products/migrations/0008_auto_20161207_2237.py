# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_application_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='introduction',
            field=DjangoUeditor.models.UEditorField(max_length=10000),
        ),
    ]
