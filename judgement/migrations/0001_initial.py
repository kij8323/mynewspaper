# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_collectioncompany'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(max_length=5000, null=True, blank=True)),
                ('introduction', models.TextField(max_length=5000, null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'images/', blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
                ('model', models.CharField(max_length=120)),
                ('image', models.ImageField(null=True, upload_to=b'images/Instrument/', blank=True)),
                ('verify', models.BooleanField(default=False, db_index=True)),
                ('introaddr', models.CharField(max_length=500)),
                ('grade', models.IntegerField(default=0)),
                ('uptime', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(to='judgement.Category')),
                ('company', models.ForeignKey(blank=True, to='company.Company', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instrumentgrade',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
                ('starall', models.IntegerField(default=0)),
                ('star1', models.IntegerField(default=0)),
                ('star2', models.IntegerField(default=0)),
                ('star3', models.IntegerField(default=0)),
                ('star4', models.IntegerField(default=0)),
                ('star5', models.IntegerField(default=0)),
                ('grade', models.IntegerField(default=0)),
                ('instrument', models.ForeignKey(to='judgement.Instrument')),
            ],
        ),
        migrations.CreateModel(
            name='Instrumentusercomment',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('instrument', models.ForeignKey(to='judgement.Instrument')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
