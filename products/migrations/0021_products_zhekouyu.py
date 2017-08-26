# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_products_oneresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='zhekouyu',
            field=models.IntegerField(default=0),
        ),
    ]
