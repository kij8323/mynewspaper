# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topic', '0018_auto_20161102_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groupmanager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(to='topic.Group')),
                ('manager', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
