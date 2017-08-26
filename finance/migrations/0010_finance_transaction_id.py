# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0009_auto_20170825_0402'),
    ]

    operations = [
        migrations.AddField(
            model_name='finance',
            name='transaction_id',
            field=models.CharField(max_length=28, null=True, blank=True),
        ),
    ]
