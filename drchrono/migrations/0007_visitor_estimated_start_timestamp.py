# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0006_auto_20180208_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='estimated_start_timestamp',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
