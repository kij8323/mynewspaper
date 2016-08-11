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
            name='CollectionInvestment',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('entitle', models.CharField(max_length=120, null=True, blank=True)),
                ('weburl', models.CharField(max_length=120)),
                ('fundtime', models.CharField(default=b'\xe2\x80\x94\xe2\x80\x94', max_length=100)),
                ('investindex', models.IntegerField(default=0, db_index=True)),
                ('introduce', ckeditor.fields.RichTextField(max_length=2000, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('logo', models.ImageField(default=b'images/companylogo.png', upload_to=b'images/', blank=True)),
                ('preference1', models.CharField(default=b'\xe2\x80\x94\xe2\x80\x94', max_length=100)),
                ('preference2', models.CharField(max_length=100, null=True, blank=True)),
                ('preference3', models.CharField(max_length=100, null=True, blank=True)),
                ('preference4', models.CharField(max_length=100, null=True, blank=True)),
                ('preference5', models.CharField(max_length=100, null=True, blank=True)),
                ('investfiled1', models.CharField(default=b'\xe2\x80\x94\xe2\x80\x94', max_length=100)),
                ('investfiled2', models.CharField(max_length=100, null=True, blank=True)),
                ('investfiled3', models.CharField(max_length=100, null=True, blank=True)),
                ('investfiled4', models.CharField(max_length=100, null=True, blank=True)),
                ('investfiled5', models.CharField(max_length=100, null=True, blank=True)),
                ('investfiled6', models.CharField(max_length=100, null=True, blank=True)),
                ('investfiled7', models.CharField(max_length=100, null=True, blank=True)),
                ('investfiled8', models.CharField(max_length=100, null=True, blank=True)),
                ('investfiled9', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='collectioninvestment',
            name='investment',
            field=models.ForeignKey(to='investment.Investment'),
        ),
        migrations.AddField(
            model_name='collectioninvestment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
