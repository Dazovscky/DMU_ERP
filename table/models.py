from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)


class Teacher(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Discipline(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Assign(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return '%s : %s : %s' % (self.teacher, self.discipline, self.group)


class AssignTime(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    time = models.IntegerField()
    day = models.CharField(choices=DAYS_OF_WEEK, max_length=150)


class AttendanceClass(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    date = models.DateField()


class Attendance(models.Model):
    attendance_class = models.ForeignKey(AttendanceClass, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.attendance_class


class AttendanceRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()



