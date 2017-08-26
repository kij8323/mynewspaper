# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_myuser_ifscore'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('fans', models.ForeignKey(related_name='fans', to=settings.AUTH_USER_MODEL)),
                ('host', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
