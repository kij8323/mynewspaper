# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20160826_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='reportnum',
            field=models.IntegerField(default=0),
        ),
    ]
