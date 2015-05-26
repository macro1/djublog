# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('language', models.CharField(null=True, max_length=100, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('statusid', models.CharField(max_length=100, editable=False)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LocalFeed',
            fields=[
                ('feed_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, to='djublog.Feed', auto_created=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            bases=('djublog.feed',),
        ),
        migrations.CreateModel(
            name='RemoteFeed',
            fields=[
                ('feed_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, to='djublog.Feed', auto_created=True)),
                ('feed_url', models.URLField()),
                ('username', models.CharField(null=True, max_length=100, editable=False)),
                ('userid', models.CharField(null=True, max_length=100, editable=False)),
                ('profile_url', models.URLField(null=True, editable=False)),
                ('build_date', models.DateTimeField(null=True, editable=False)),
                ('raw_feed', models.TextField(null=True, editable=False)),
            ],
            bases=('djublog.feed',),
        ),
        migrations.AddField(
            model_name='post',
            name='feed',
            field=models.ForeignKey(to='djublog.Feed'),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('feed', 'statusid')]),
        ),
    ]
