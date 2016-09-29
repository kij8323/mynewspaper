# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20160826_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
