# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_products_reportnum'),
        ('topic', '0015_auto_20160606_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='products',
            field=models.ForeignKey(blank=True, to='products.Products', null=True),
        ),
    ]
