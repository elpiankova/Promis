# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geoprom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('sampling_frequency', models.FloatField(null=True, blank=True)),
            ],
            options={
                'ordering': ['title', 'device'],
                'db_table': 'channels',
            },
        ),
        migrations.CreateModel(
            name='ChannelOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=45)),
                ('value', models.CharField(null=True, db_column='co_value', blank=True, max_length=45)),
                ('description', models.TextField(null=True, blank=True)),
                ('channel', models.ForeignKey(to='geoprom.Channel')),
            ],
            options={
                'db_table': 'channels_options',
            },
        ),
        migrations.CreateModel(
            name='ChannelsHaveSessions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='geoprom.Channel', related_name='+')),
            ],
            options={
                'db_table': 'channels_have_sessions',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['title'],
                'db_table': 'devices',
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('title', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('short_name', models.CharField(max_length=25)),
                ('level', models.IntegerField()),
                ('description', models.TextField(null=True, blank=True, max_length=255)),
            ],
            options={
                'db_table': 'parameters',
            },
        ),
        migrations.CreateModel(
            name='ParentChildRel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, db_column='child_title', to='geoprom.Parameter', related_name='child+')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, db_column='parent_title', to='geoprom.Parameter', related_name='parent+')),
            ],
            options={
                'db_table': 'parameters_have_parameters',
            },
        ),
        migrations.CreateModel(
            name='Satellite',
            fields=[
                ('title', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('highlighted', models.TextField()),
                ('owner', models.ForeignKey(related_name='satellites', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'satellites',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('code', models.CharField(max_length=6)),
                ('time_begin', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('geo_line', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
            ],
            options={
                'ordering': ['time_begin', 'time_end', 'geo_line'],
                'db_table': 'sessions',
            },
        ),
        migrations.CreateModel(
            name='SessionOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('value', models.CharField(null=True, db_column='so_value', blank=True, max_length=255)),
                ('session', models.ForeignKey(to='geoprom.Session')),
            ],
            options={
                'db_table': 'sessions_options',
            },
        ),
        migrations.CreateModel(
            name='SessionsHaveParameters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='geoprom.Parameter', related_name='+')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='geoprom.Session', related_name='+')),
            ],
            options={
                'db_table': 'sessions_have_parameters',
            },
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('title', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('short_name', models.CharField(max_length=45)),
                ('long_name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'units',
                'db_table': 'units',
            },
        ),
        migrations.DeleteModel(
            name='WorldBorder',
        ),
        migrations.AddField(
            model_name='session',
            name='parameters',
            field=models.ManyToManyField(to='geoprom.Parameter', through='geoprom.SessionsHaveParameters'),
        ),
        migrations.AddField(
            model_name='parameter',
            name='units',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, db_column='units_title', to='geoprom.Units'),
        ),
        migrations.AddField(
            model_name='device',
            name='satellite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, db_column='satellite_title', to='geoprom.Satellite'),
        ),
        migrations.AddField(
            model_name='channelshavesessions',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='geoprom.Session', related_name='+'),
        ),
        migrations.AddField(
            model_name='channel',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='geoprom.Device'),
        ),
        migrations.AddField(
            model_name='channel',
            name='sessions',
            field=models.ManyToManyField(to='geoprom.Session', through='geoprom.ChannelsHaveSessions'),
        ),
        migrations.AlterUniqueTogether(
            name='sessionshaveparameters',
            unique_together=set([('session', 'parameter')]),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('time_begin', 'time_end', 'geo_line')]),
        ),
        migrations.AlterUniqueTogether(
            name='parentchildrel',
            unique_together=set([('parent', 'child')]),
        ),
        migrations.AlterUniqueTogether(
            name='device',
            unique_together=set([('title', 'satellite')]),
        ),
        migrations.AlterUniqueTogether(
            name='channelshavesessions',
            unique_together=set([('channel', 'session')]),
        ),
        migrations.AlterUniqueTogether(
            name='channel',
            unique_together=set([('title', 'device')]),
        ),
    ]
