# Generated by Django 2.0.4 on 2018-11-09 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0014_auto_20181106_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='clinic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.Clinic'),
        ),
    ]
