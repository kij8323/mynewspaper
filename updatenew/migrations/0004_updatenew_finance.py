# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_finance_qrcodeimage'),
        ('updatenew', '0003_updatenew_instrument'),
    ]

    operations = [
        migrations.AddField(
            model_name='updatenew',
            name='finance',
            field=models.ForeignKey(blank=True, to='finance.Finance', null=True),
        ),
    ]
