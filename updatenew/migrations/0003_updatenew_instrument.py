# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judgement', '0002_auto_20170415_1720'),
        ('updatenew', '0002_updatenew_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='updatenew',
            name='instrument',
            field=models.ForeignKey(blank=True, to='judgement.Instrument', null=True),
        ),
    ]
