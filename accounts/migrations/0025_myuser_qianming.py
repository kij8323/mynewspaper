# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_remove_myuser_qianming'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='qianming',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
