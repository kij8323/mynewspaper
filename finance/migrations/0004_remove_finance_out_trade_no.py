# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_auto_20170601_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finance',
            name='out_trade_no',
        ),
    ]
