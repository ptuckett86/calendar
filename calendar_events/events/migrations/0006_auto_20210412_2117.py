# Generated by Django 3.2 on 2021-04-12 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20210412_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='calendarevent',
            name='event_type',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='calendarevent',
            name='notes',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
