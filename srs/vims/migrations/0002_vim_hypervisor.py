# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-05 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('vims', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vim',
            name='hypervisor',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]