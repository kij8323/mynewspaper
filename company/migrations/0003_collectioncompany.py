# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0002_auto_20160714_2351'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionCompany',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
                ('company', models.ForeignKey(to='company.Company')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
