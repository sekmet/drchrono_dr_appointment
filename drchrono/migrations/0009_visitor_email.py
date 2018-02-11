# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0008_auto_20180208_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='email',
            field=models.EmailField(default=datetime.datetime(2018, 2, 9, 21, 19, 49, 969000, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
