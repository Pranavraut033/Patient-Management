# Generated by Django 2.0.4 on 2018-11-05 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0006_auto_20181105_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='abbreviation',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]