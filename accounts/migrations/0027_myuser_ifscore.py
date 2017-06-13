# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_auto_20170402_0243'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='ifscore',
            field=models.BooleanField(default=False),
        ),
    ]
