# Generated by Django 2.0.4 on 2018-08-27 19:04

import clinic.utils.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0015_auto_20180828_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='human',
            name='email',
            field=models.CharField(blank=True, max_length=40, validators=[clinic.utils.validators.validate_email], verbose_name='Email Address'),
        ),
    ]
