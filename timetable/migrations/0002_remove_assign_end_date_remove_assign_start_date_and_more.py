# Generated by Django 4.0 on 2023-01-29 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assign',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='assign',
            name='start_date',
        ),
        migrations.AddField(
            model_name='assigntime',
            name='end_date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assigntime',
            name='start_date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendanceclass',
            name='assign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.assign'),
        ),
    ]
