# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discovery',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('img', models.ImageField(default=b'images/78avatarbig.jpg', max_length=1000, null=True, upload_to=b'discovery/img/', blank=True)),
                ('title', models.CharField(max_length=120)),
                ('count', models.CharField(max_length=120)),
                ('addr', models.CharField(max_length=1200)),
                ('price', models.CharField(max_length=120)),
                ('infor', models.CharField(max_length=120, null=True, blank=True)),
                ('amount', models.CharField(max_length=120)),
                ('verify', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Discoveryhost',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('icon', models.ImageField(default=b'images/78avatarbig.jpg', null=True, upload_to=b'discovery/img/', blank=True)),
                ('title', models.CharField(max_length=120)),
                ('addr', models.CharField(max_length=1200)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='discovery',
            name='host',
            field=models.ForeignKey(to='discovery.Discoveryhost'),
        ),
    ]
