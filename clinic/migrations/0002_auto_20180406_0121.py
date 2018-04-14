# Generated by Django 2.0.3 on 2018-04-05 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FromSys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='From System')),
            ],
        ),
        migrations.AddField(
            model_name='disease',
            name='from_system',
            field=models.ForeignKey(default=None, on_delete=models.SET(None), to='clinic.FromSys'),
            preserve_default=False,
        ),
    ]