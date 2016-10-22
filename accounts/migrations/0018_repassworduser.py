# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20161001_0258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repassworduser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255)),
                ('userid', models.CharField(max_length=255)),
                ('phonenumber', models.CharField(max_length=255)),
            ],
        ),
    ]
