# Generated by Django 2.0.4 on 2018-08-23 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0008_remove_followup_gift'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followup',
            name='fee',
        ),
        migrations.AddField(
            model_name='followup',
            name='fees',
            field=models.PositiveSmallIntegerField(default=100),
        ),
    ]
