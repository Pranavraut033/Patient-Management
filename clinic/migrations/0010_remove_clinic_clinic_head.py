# Generated by Django 2.0.4 on 2018-11-06 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0009_auto_20181105_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clinic',
            name='clinic_head',
        ),
    ]
