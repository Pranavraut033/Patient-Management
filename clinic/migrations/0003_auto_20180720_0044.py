# Generated by Django 2.0.4 on 2018-07-19 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_auto_20180720_0042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='human',
            name='address',
        ),
        migrations.AddField(
            model_name='human',
            name='s_address',
            field=models.CharField(default='', max_length=100, verbose_name='Street Address'),
            preserve_default=False,
        ),
    ]
