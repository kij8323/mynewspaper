# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_payscorerec'),
        ('updatenew', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='updatenew',
            name='products',
            field=models.ForeignKey(blank=True, to='products.Products', null=True),
        ),
    ]
