# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_products_one'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='ifapply',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name='products',
            name='ifone',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name='products',
            name='oneamount',
            field=models.IntegerField(default=0),
        ),
    ]
