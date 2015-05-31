# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djublog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='statusid',
            new_name='guid',
        ),
        migrations.AddField(
            model_name='basefeed',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='basefeed',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='basefeed',
            name='language',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('feed', 'guid')]),
        ),
    ]
