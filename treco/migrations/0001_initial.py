# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import treco.validator


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('display_name', models.CharField(max_length=16, unique=True, serialize=False, primary_key=True)),
                ('profile_picture', models.ImageField(upload_to=b'profile_pictures')),
                ('website', models.URLField(default=b'', max_length=128)),
                ('organization', models.CharField(default=b'', max_length=64)),
                ('userid', models.OneToOneField(db_column=b'id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=64)),
                ('description', models.CharField(default=b'', max_length=256)),
                ('result_file', models.FileField(upload_to=b'result_files', validators=[treco.validator.validateResultFile])),
                ('run_type', models.CharField(max_length=1, choices=[(b'0', b'Automatic'), (b'1', b'Manual')])),
                ('query_type', models.CharField(max_length=32, choices=[(b'0', b'Title'), (b'1', b'Title and Description'), (b'2', b'Description'), (b'3', b'All'), (b'4', b'Other')])),
                ('feedback_type', models.CharField(max_length=32, choices=[(b'0', b'None'), (b'1', b'Psuedo'), (b'2', b'Relevance'), (b'3', b'Other')])),
                ('map', models.FloatField()),
                ('p10', models.FloatField()),
                ('p20', models.FloatField()),
                ('researcher', models.ForeignKey(to='treco.Researcher', db_column=b'display_name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_title', models.CharField(default=b'', max_length=32, unique=True, serialize=False, primary_key=True)),
                ('task_url', models.SlugField()),
                ('description', models.CharField(default=b'', max_length=128)),
                ('year', models.IntegerField(max_length=4)),
                ('judgement_file', models.FileField(upload_to=b'judgement_files', validators=[treco.validator.validateJudgementFile])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('track_title', models.CharField(max_length=32, unique=True, serialize=False, primary_key=True)),
                ('track_url', models.SlugField()),
                ('description', models.CharField(default=b'', max_length=128)),
                ('genre', models.CharField(default=b'', max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='track',
            field=models.ForeignKey(to='treco.Track', db_column=b'track_title'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='run',
            name='task',
            field=models.ForeignKey(to='treco.Task'),
            preserve_default=True,
        ),
    ]
