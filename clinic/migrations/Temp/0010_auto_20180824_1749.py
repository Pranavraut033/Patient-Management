# Generated by Django 2.0.4 on 2018-08-24 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0009_auto_20180824_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='human',
            name='profile',
            field=models.ImageField(blank=True, default='profile_pictures/generic-user.png', upload_to='clinic/profile_pictures/'),
        ),
    ]
