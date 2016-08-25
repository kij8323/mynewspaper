# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_collectioncompany'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('introduction', ckeditor.fields.RichTextField(max_length=20000, null=True)),
                ('price', models.IntegerField(default=0)),
                ('amount', models.IntegerField(default=0)),
                ('verify', models.BooleanField(default=False, db_index=True)),
                ('status', models.IntegerField(default=1)),
                ('periods', models.IntegerField(default=1)),
                ('picture', models.ImageField(default=b'images/companylogo.png', upload_to=b'images/', blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('timedeadline', models.DateTimeField(null=True)),
                ('company', models.ForeignKey(blank=True, to='company.Company', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='products',
            field=models.ForeignKey(to='products.Products'),
        ),
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
