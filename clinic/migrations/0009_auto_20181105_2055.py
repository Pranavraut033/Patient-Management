# Generated by Django 2.0.4 on 2018-11-05 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0008_auto_20181105_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caseappointment',
            name='custom_location',
            field=models.CharField(blank=True, default="", max_length=50),
            preserve_default=False,
        ),
    ]
