# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_payscorerec'),
        ('finance', '0002_finance_testchar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='finance',
            old_name='tradeno',
            new_name='out_trade_no',
        ),
        migrations.RemoveField(
            model_name='finance',
            name='testchar',
        ),
        migrations.AddField(
            model_name='finance',
            name='buyer_id',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finance',
            name='out_biz_no',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finance',
            name='products',
            field=models.ForeignKey(blank=True, to='products.Products', null=True),
        ),
        migrations.AddField(
            model_name='finance',
            name='receipt_amount',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finance',
            name='total_amount',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finance',
            name='trade_no',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finance',
            name='trade_status',
            field=models.BooleanField(default=False),
        ),
    ]
