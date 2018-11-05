# Generated by Django 2.0.4 on 2018-11-04 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0003_auto_20181104_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.Address')),
            ],
        ),
        migrations.RemoveField(
            model_name='person',
            name='address',
        ),
        migrations.AddField(
            model_name='personaddress',
            name='person',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.Person'),
        ),
    ]
