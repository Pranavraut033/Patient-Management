# Generated by Django 2.0.4 on 2018-11-04 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0004_auto_20181104_1103'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonPhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='person',
            name='phone_number',
        ),
        migrations.AlterField(
            model_name='personaddress',
            name='address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.Address'),
        ),
        migrations.AlterField(
            model_name='personaddress',
            name='person',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.Person'),
        ),
        migrations.AddField(
            model_name='personphonenumber',
            name='person',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.Person'),
        ),
        migrations.AddField(
            model_name='personphonenumber',
            name='phone_number',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.PhoneNumber'),
        ),
    ]
