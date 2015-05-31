# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('djublog', '0002_auto_20150530_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 31, 3, 28, 14, 126020, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
