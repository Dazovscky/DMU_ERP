from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
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
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        te = Teacher.objects.get(id=self.teacher_id)
        di = Discipline.objects.get(id=self.discipline_id)
        gr = Group.objects.get(id=self.group_id)
        return '%s : %s : %s' % (te.name, di.name, gr.name)


class AssignTime(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    time = models.IntegerField()
    day = models.CharField(choices=DAYS_OF_WEEK, max_length=150)

    def __str__(self):
        return '%s : %s' % (self.assign, self.day)


class AttendanceClass(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    date = models.DateField()


class Attendance(models.Model):
    attendance_class = models.ForeignKey(AttendanceClass, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return '%s' % self.attendance_class

 
class AttendanceRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


days = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
}


def create_attendance(sender, instance, **kwargs):
    if kwargs['created']:
        start_date = AttendanceRange.objects.all()[:1].get().start_date
        end_date = AttendanceRange.objects.all()[:1].get().end_date
        for single_date in daterange(start_date, end_date):
            if single_date.isoweekday() == days[instance.day]:
                try:
                    AttendanceClass.objects.get(date=single_date.strftime("%Y-%m-%d"), assign=instance.assign)
                except AttendanceClass.DoesNotExist:
                    a = AttendanceClass(date=single_date.strftime("%Y-%m-%d"), assign=instance.assign)
                    a.save()


post_save.connect(create_attendance, sender=AssignTime)