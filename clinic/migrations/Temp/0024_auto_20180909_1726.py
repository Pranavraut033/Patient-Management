# Generated by Django 2.0.4 on 2018-09-09 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0023_auto_20180909_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='speciality',
            field=models.CharField(choices=[('ped', 'Pediatrics'), ('crl', 'Cardiologist'), ('gyl', 'Gynaecolgist'), ('nrl', 'Neurologist'), ('ocl', 'Oncologist'), ('phy', 'Physician'), ('nes', 'Neuro Surgeon'), ('ges', 'General Surgeon'), ('gep', 'General Practitioner')], max_length=3, verbose_name='Practitioner type'),
        ),
        migrations.AlterField(
            model_name='human',
            name='blood_type',
            field=models.SmallIntegerField(blank=True, choices=[(-1, 'Unknown'), (0, 'A+'), (1, 'B+'), (2, 'AB+'), (3, 'O+'), (4, 'A-'), (5, 'B-'), (6, 'AB-'), (7, 'O-')]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='er_rel',
            field=models.CharField(choices=[('S', 'Sprouse'), ('P', 'Parent'), ('Si', 'Sibling'), ('G', 'Guardian'), ('O', 'Other')], max_length=2, verbose_name='Relationship with the Emergency contact'),
        ),
    ]
