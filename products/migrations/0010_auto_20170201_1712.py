# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0009_auto_20161215_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payscore',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
                ('payscore', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='ifscore',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name='products',
            name='scoreamount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='products',
            name='scoreing',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='payscore',
            name='products',
            field=models.ForeignKey(to='products.Products'),
        ),
        migrations.AddField(
            model_name='payscore',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
