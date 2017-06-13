# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_payscorerec'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='one',
            field=models.IntegerField(default=0),
        ),
    ]
