# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judgement', '0001_initial'),
        ('notifications', '0016_notification_target_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='target_instrument',
            field=models.ForeignKey(blank=True, to='judgement.Instrument', null=True),
        ),
    ]
