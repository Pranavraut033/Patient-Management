# Generated by Django 2.0.4 on 2018-11-05 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0003_auto_20181105_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='profile',
            field=models.ImageField(default='clinic/static/clinic/user_profile/no-profile.png', upload_to='clinic/static/clinic/user_profile/'),
        ),
    ]
