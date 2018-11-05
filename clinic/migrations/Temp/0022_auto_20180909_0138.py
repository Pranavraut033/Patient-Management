# Generated by Django 2.0.4 on 2018-09-08 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0021_auto_20180909_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='human',
            name='blood_group',
            field=models.SmallIntegerField(choices=[(-1, 'Unknown'), (0, 'A+'), (1, 'B+'), (2, 'AB+'), (3, 'O+'), (4, 'A-'), (5, 'B-'), (6, 'AB-'), (7, 'O-')], default=-1, verbose_name='Blood Group'),
        ),
    ]