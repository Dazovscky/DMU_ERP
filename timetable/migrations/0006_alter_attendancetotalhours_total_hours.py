# Generated by Django 4.0 on 2023-01-30 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0005_attendancetotalhours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancetotalhours',
            name='total_hours',
            field=models.IntegerField(default=0),
        ),
    ]