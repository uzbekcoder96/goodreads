# Generated by Django 4.0 on 2022-02-19 03:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_book_pcture'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreview',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 19, 3, 50, 2, 165629, tzinfo=utc)),
        ),
    ]
