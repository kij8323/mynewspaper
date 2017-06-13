# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_remove_finance_out_trade_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='finance',
            name='out_trade_no',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
    ]
