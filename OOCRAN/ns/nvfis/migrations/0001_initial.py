# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-23 07:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('operators', '0001_initial'),
        ('scenarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NVFI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to='opnfv/')),
                ('status', models.CharField(default='Shut Down', max_length=120)),
                ('type', models.CharField(blank=True, default='Local', max_length=120, null=True)),
                ('price', models.FloatField(default=0)),
                ('graph', models.TextField(blank=True, null=True)),
                ('launch_time', models.DateTimeField(blank=True, null=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operators.Operator')),
                ('scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenarios.Scenario')),
            ],
            options={
                'ordering': ['-timestamp', '-update'],
            },
        ),
    ]
