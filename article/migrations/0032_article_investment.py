# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0001_initial'),
        ('article', '0031_article_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='investment',
            field=models.ForeignKey(blank=True, to='investment.Investment', null=True),
        ),
    ]
