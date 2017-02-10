# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(unique=True, choices=[('Wave probe WP(count3)', 'Wave probe WP(count3)'), ('Electric  probe', 'Electric  probe'), ('Radio frequency analyser', 'Radio frequency analyser'), ('Neutral component plasma probe', 'Neutral component plasma probe'), ('Electric component plasma probes', 'Electric component plasma probes'), ('Flux-Gate magnetometer constant field', 'Flux-Gate magnetometer constant field'), ('Total electron content', 'Total electron content'), ('System for gathering scientific information', 'System for gathering scientific information')], max_length=255)),
                ('code', models.CharField(unique=True, max_length=6)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'devices',
            },
        ),
        migrations.CreateModel(
            name='DeviceMode',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=6)),
                ('device', models.ForeignKey(to='request_creation.Device', related_name='modes')),
            ],
            options={
                'db_table': 'device_modes',
            },
        ),
        migrations.CreateModel(
            name='DeviceSwitch',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('argument_part_len', models.SmallIntegerField()),
                ('time_delay', models.DurationField()),
                ('time_duration', models.DurationField()),
                ('argument_part', models.CharField(max_length=620)),
                ('device', models.ForeignKey(to='request_creation.Device')),
                ('mode', models.ForeignKey(to='request_creation.DeviceMode')),
            ],
            options={
                'db_table': 'device_switches',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('number', models.SmallIntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(9999, message='Request number must be less than 9999')])),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('orbit_flag', models.CharField(default='p', choices=[('y', 'upward'), ('n', 'downward'), ('p', 'any')], max_length=1)),
                ('latitude_start', models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MaxValueValidator(82.0, message='Request latitude start must be less then 82.0'), django.core.validators.MinValueValidator(-82.0, message='Request latitude start must be greater than -82.0')])),
                ('longitude_left', models.DecimalField(decimal_places=1, max_digits=4, validators=[django.core.validators.MaxValueValidator(359.0, message='Request longitude stop must be less then 359.0'), django.core.validators.MinValueValidator(0.0, message='Request longitude start must be greater then 000.0')])),
                ('longitude_right', models.DecimalField(decimal_places=1, max_digits=4, validators=[django.core.validators.MaxValueValidator(359.0, message='Request longitude stop must be less then 359.0'), django.core.validators.MinValueValidator(0.0, message='Request longitude start must be greater then 000.0')])),
                ('device_amount', models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(8, message='Request device amount must be in range 1-8'), django.core.validators.MinValueValidator(1, message='Request device amount must be in range 1-8')])),
                ('request_file', models.FilePathField(path='/home/mammut/Site/Promis/ionosat_request/request_files', validators=[django.core.validators.RegexValidator('KNA(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[012])\\d\\d\\d{4}\\.zp', message='Request file name should be KNAddmmyynnnn.zp')])),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'requests',
            },
        ),
        migrations.AddField(
            model_name='deviceswitch',
            name='request',
            field=models.ForeignKey(to='request_creation.Request', related_name='switches'),
        ),
        migrations.AlterUniqueTogether(
            name='deviceswitch',
            unique_together=set([('device', 'request')]),
        ),
        migrations.AlterUniqueTogether(
            name='devicemode',
            unique_together=set([('device', 'name')]),
        ),
    ]
