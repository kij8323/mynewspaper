# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topic', '0034_topic_img1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daka',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
                ('date', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
