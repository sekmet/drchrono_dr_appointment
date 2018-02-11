# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0003_auto_20180207_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='create_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 7, 21, 20, 42, 407000)),
        ),
    ]
