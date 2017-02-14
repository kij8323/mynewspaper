# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20170119_2210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='qianming',
        ),
    ]
