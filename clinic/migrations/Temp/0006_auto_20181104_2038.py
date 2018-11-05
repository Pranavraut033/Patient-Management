# Generated by Django 2.0.4 on 2018-11-04 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0005_auto_20181104_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.Visit')),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyContactPhone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameModel(
            old_name='Timming',
            new_name='BranchTimming',
        ),
        migrations.RenameModel(
            old_name='PersonPhoneNumber',
            new_name='PersonPhone',
        ),
        migrations.RenameModel(
            old_name='VisitStatement',
            new_name='Statement',
        ),
        migrations.RemoveField(
            model_name='subcomplaint',
            name='serverity',
        ),
        migrations.RemoveField(
            model_name='subcomplaint',
            name='status',
        ),
        migrations.RemoveField(
            model_name='subcomplaint',
            name='symptom',
        ),
        migrations.RemoveField(
            model_name='subcomplaint',
            name='visit',
        ),
        migrations.RemoveField(
            model_name='visitdisease',
            name='disease',
        ),
        migrations.RemoveField(
            model_name='visitdisease',
            name='visit',
        ),
        migrations.RemoveField(
            model_name='visitmedicine',
            name='medicine',
        ),
        migrations.RemoveField(
            model_name='visitmedicine',
            name='visit',
        ),
        migrations.RenameField(
            model_name='case',
            old_name='reg_date',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='branch',
            name='address',
        ),
        migrations.RemoveField(
            model_name='emergencycontact',
            name='er_number',
        ),
        migrations.AddField(
            model_name='case',
            name='recomnendation',
            field=models.CharField(blank=True, max_length=180),
        ),
        migrations.AddField(
            model_name='case',
            name='title',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='disease',
            name='visit',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='clinic.Visit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drug',
            name='visit',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='clinic.Visit'),
            preserve_default=False,
        ),
        migrations.RenameModel(
            old_name='PhoneNumber',
            new_name='Phone',
        ),
        migrations.DeleteModel(
            name='SubComplaint',
        ),
        migrations.DeleteModel(
            name='VisitDisease',
        ),
        migrations.DeleteModel(
            name='VisitMedicine',
        ),
        migrations.AddField(
            model_name='emergencycontactphone',
            name='emergency_contact',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.EmergencyContact'),
        ),
        migrations.AddField(
            model_name='emergencycontactphone',
            name='phone_number',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.Phone'),
        ),
        migrations.AddField(
            model_name='serverity',
            name='complaint',
            field=models.ManyToManyField(to='clinic.Complaint'),
        ),
        migrations.AddField(
            model_name='status',
            name='complaint',
            field=models.ManyToManyField(to='clinic.Complaint'),
        ),
        migrations.AddField(
            model_name='symptom',
            name='complaint',
            field=models.ManyToManyField(to='clinic.Complaint'),
        ),
    ]
