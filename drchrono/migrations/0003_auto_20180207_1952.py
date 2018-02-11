# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0002_auto_20180205_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='finish_treatment_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 8, 3, 52, 29, 363000, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visitor',
            name='start_treatment_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 8, 3, 52, 44, 865000, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='visitor',
            name='create_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 7, 19, 52, 14, 238000)),
        ),
    ]
