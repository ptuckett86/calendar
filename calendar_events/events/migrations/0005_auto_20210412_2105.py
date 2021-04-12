# Generated by Django 3.2 on 2021-04-12 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_rename_summary_calendarevent_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='dt_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='calendarevent',
            name='dt_start',
            field=models.DateTimeField(help_text='Will store as UTC, set TZ on front end and process to UTC.'),
        ),
    ]