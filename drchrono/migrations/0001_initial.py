# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('visit_timestamp', models.DateTimeField(default=None, null=True)),
                ('visit_date', models.DateField(auto_now_add=True)),
                ('is_appointment', models.BooleanField(default=False)),
                ('duration', models.DecimalField(default=30, max_digits=5, decimal_places=0)),
                ('drchrono_appointment_page', models.CharField(max_length=200)),
            ],
        ),
    ]
