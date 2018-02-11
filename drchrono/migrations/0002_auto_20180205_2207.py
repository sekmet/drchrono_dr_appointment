# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitor',
            name='visit_date',
        ),
        migrations.RemoveField(
            model_name='visitor',
            name='visit_timestamp',
        ),
        migrations.AddField(
            model_name='visitor',
            name='appointment_data',
            field=models.CharField(max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='visitor',
            name='create_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 5, 22, 7, 58, 797000)),
        ),
        migrations.AddField(
            model_name='visitor',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='visitor',
            name='is_confirmed',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='visitor',
            name='is_queue',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='visitor',
            name='sympton',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='drchrono_appointment_page',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
