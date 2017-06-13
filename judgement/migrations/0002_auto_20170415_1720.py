# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('judgement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='uper',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='instrument',
            name='usercompany',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='category',
            field=models.ForeignKey(blank=True, to='judgement.Category', null=True),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='introaddr',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='uptime',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
