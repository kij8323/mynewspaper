# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        ('article', '0030_auto_20160527_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='company',
            field=models.ForeignKey(blank=True, to='company.Company', null=True),
        ),
    ]
