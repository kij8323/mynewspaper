# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0007_auto_20170619_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finance',
            name='out_biz_no',
            field=models.CharField(max_length=6400, null=True, blank=True),
        ),
    ]
