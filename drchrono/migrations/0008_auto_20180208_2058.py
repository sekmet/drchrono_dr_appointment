# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0007_visitor_estimated_start_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='duration',
            field=models.IntegerField(default=30),
        ),
    ]
