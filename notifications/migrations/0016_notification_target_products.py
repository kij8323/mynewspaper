# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('notifications', '0015_auto_20160503_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='target_products',
            field=models.ForeignKey(blank=True, to='products.Products', null=True),
        ),
    ]
