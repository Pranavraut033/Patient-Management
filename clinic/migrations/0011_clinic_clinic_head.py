# Generated by Django 2.0.4 on 2018-11-06 03:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0010_remove_clinic_clinic_head'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='clinic_head',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='clinic.Doctor'),
            preserve_default=False,
        ),
    ]
