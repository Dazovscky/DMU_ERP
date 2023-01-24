# Generated by Django 4.0 on 2023-01-28 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assign_view', models.CharField(choices=[('Лекция', 'Лекция'), ('Prac', 'Prac')], max_length=15, null=True)),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], max_length=15)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='AssignTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(choices=[('09.00 - 10.20', '09.00 - 10.20'), ('10.50 - 12.10', '10.50 - 12.10'), ('12.55 - 14.15', '12.55 - 14.15'), ('14.45 - 16.05', '14.45 - 16.05')], max_length=50)),
                ('assign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.assign')),
            ],
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_name', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_name', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_name', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('assign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.assigntime')),
            ],
        ),
        migrations.AddField(
            model_name='assign',
            name='discipline',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable.discipline'),
        ),
        migrations.AddField(
            model_name='assign',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable.group'),
        ),
        migrations.AddField(
            model_name='assign',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable.teacher'),
        ),
    ]