# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_finance_qrcodeimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='finance',
            name='end',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='finance',
            name='start',
            field=models.IntegerField(default=0),
        ),
    ]
