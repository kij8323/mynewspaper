# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_products_tryamount'),
    ]

    operations = [
        migrations.AddField(
            model_name='payscore',
            name='win',
            field=models.BooleanField(default=False),
        ),
    ]
