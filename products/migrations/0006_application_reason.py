# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_products_reportnum'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='reason',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
