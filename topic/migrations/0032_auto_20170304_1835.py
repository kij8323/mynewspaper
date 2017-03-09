# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0031_group_glyphicon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmanager',
            name='manager',
            field=models.ForeignKey(default=2028, to=settings.AUTH_USER_MODEL),
        ),
    ]
