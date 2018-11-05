# Generated by Django 2.0.4 on 2018-09-03 10:00

import clinic.utils.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0016_auto_20180828_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='speciality',
            field=models.CharField(choices=[('ped', 'Pediatrics'), ('crl', 'Cardiologist'), ('gyl', 'Gynaecolgist'), ('nrl', 'Neurologist'), ('ocl', 'Oncologist'), ('phy', 'Physician'), ('nes', 'Neuro Surgeon'), ('ges', 'General Surgeon'), ('gep', 'General Practitioner')], default='gp', max_length=3, verbose_name='Medical specialties'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='username',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, validators=[clinic.utils.validators.validate_username]),
        ),
        migrations.AlterField(
            model_name='human',
            name='phone_number',
            field=models.BigIntegerField(validators=[clinic.utils.validators.validate_number]),
        ),
        migrations.AlterField(
            model_name='human',
            name='pincode',
            field=models.IntegerField(validators=[clinic.utils.validators.validate_pincode]),
        ),
    ]
