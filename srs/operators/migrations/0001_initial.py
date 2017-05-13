# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-01 08:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('password', models.CharField(max_length=120)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('vnfm', models.CharField(max_length=120)),
                ('vagrant_hypervisor', models.CharField(max_length=120)),
                ('price', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('operator_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='operators.Operator')),
                ('spectrum', models.FloatField(default=0)),
                ('network', models.FloatField(default=0)),
                ('cpu', models.FloatField(default=0)),
                ('ram', models.FloatField(default=0)),
            ],
            bases=('operators.operator',),
        ),
        migrations.AddField(
            model_name='operator',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]