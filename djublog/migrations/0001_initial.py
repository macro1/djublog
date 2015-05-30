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
            name='BaseFeed',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('language', models.CharField(null=True, editable=False, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('statusid', models.CharField(editable=False, max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LocalFeed',
            fields=[
                ('basefeed_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, primary_key=True, to='djublog.BaseFeed')),
                ('user', models.OneToOneField(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('djublog.basefeed',),
        ),
        migrations.CreateModel(
            name='RemoteFeed',
            fields=[
                ('basefeed_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, primary_key=True, to='djublog.BaseFeed')),
                ('feed_url', models.URLField()),
                ('username', models.CharField(null=True, editable=False, max_length=100)),
                ('userid', models.CharField(null=True, editable=False, max_length=100)),
                ('profile_url', models.URLField(null=True, editable=False)),
                ('build_date', models.DateTimeField(null=True, editable=False)),
                ('raw_feed', models.TextField(null=True, editable=False)),
            ],
            bases=('djublog.basefeed',),
        ),
        migrations.AddField(
            model_name='post',
            name='feed',
            field=models.ForeignKey(to='djublog.BaseFeed'),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('feed', 'statusid')]),
        ),
    ]
