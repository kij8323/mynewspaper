# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0019_comment_grade'),
        ('judgement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='instrument',
            field=models.ForeignKey(blank=True, to='judgement.Instrument', null=True),
        ),
    ]
