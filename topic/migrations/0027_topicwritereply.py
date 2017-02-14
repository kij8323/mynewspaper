# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topic', '0026_topicusercomment_topicwritescorem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topicwritereply',
            fields=[
                ('id', models.AutoField(db_index=True, serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('topic', models.ForeignKey(to='topic.Topic')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
