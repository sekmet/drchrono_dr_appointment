# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0004_auto_20180207_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='create_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 7, 21, 33, 9, 425000)),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='finish_treatment_timestamp',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='start_treatment_timestamp',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
