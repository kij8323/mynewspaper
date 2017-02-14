# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_payscore_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='picturehome',
            field=models.ImageField(default=b'images/companylogo.png', upload_to=b'images/', blank=True),
        ),
    ]
