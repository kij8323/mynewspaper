# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('weburl', models.CharField(max_length=120)),
                ('location', models.CharField(max_length=120, null=True, db_index=True)),
                ('financing', models.CharField(db_index=True, max_length=120, null=True, blank=True)),
                ('industry', models.CharField(max_length=120, null=True, db_index=True)),
                ('associatetitle', models.CharField(max_length=120, null=True)),
                ('product', ckeditor.fields.RichTextField(max_length=2000, null=True)),
                ('pastfinancing', ckeditor.fields.RichTextField(max_length=2000, null=True, blank=True)),
                ('client', ckeditor.fields.RichTextField(max_length=2000, null=True)),
                ('future', ckeditor.fields.RichTextField(max_length=2000, null=True, blank=True)),
                ('sameproduct', ckeditor.fields.RichTextField(max_length=2000, null=True, blank=True)),
                ('connection', models.CharField(max_length=120, null=True, blank=True)),
                ('qita', ckeditor.fields.RichTextField(max_length=2000, null=True, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('team', ckeditor.fields.RichTextField(max_length=2000, null=True, blank=True)),
                ('readers', models.IntegerField(default=0)),
                ('verify', models.BooleanField(default=False, db_index=True)),
                ('logo', models.ImageField(default=b'images/companylogo.png', upload_to=b'images/', blank=True)),
                ('images1', models.ImageField(default=b'images/companylogo.png', null=True, upload_to=b'images/', blank=True)),
                ('images2', models.ImageField(default=b'images/companylogo.png', null=True, upload_to=b'images/', blank=True)),
                ('images3', models.ImageField(default=b'images/companylogo.png', null=True, upload_to=b'images/', blank=True)),
                ('wechat', models.ImageField(null=True, upload_to=b'images/', blank=True)),
                ('uper', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
