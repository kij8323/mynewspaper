# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0030_auto_20170221_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='glyphicon',
            field=models.CharField(default=b'glyphicon-folder-open', max_length=120),
        ),
    ]
