# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_finance_out_trade_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='finance',
            name='qrcodeimage',
            field=models.ImageField(null=True, upload_to=b'images/qrcode/', blank=True),
        ),
    ]
