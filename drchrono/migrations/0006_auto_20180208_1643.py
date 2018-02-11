# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0005_auto_20180207_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='create_timestamp',
            field=models.DateTimeField(),
        ),
    ]
