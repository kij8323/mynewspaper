# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('comment', '0017_auto_20160523_2355'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='products',
            field=models.ForeignKey(blank=True, to='products.Products', null=True),
        ),
    ]
