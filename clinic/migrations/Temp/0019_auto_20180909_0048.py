# Generated by Django 2.0.4 on 2018-09-08 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0018_auto_20180909_0027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='relation',
        ),
        migrations.AddField(
            model_name='patient',
            name='re_rel',
            field=models.CharField(blank=True, max_length=10, verbose_name='Relation with the Emergency contact'),
        ),
    ]
