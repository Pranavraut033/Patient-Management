# Generated by Django 2.0.4 on 2018-07-19 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='human',
            old_name='pin_code',
            new_name='pincode',
        ),
    ]
