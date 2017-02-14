# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0035_auto_20170107_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='writer',
            field=models.ForeignKey(default=2028, to=settings.AUTH_USER_MODEL),
        ),
    ]
