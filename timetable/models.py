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

ASSIGN_VIEW = (
    ('Лекция', 'Лекция'),
    ('Prac', 'Prac')
)

time_slots = (
    ('09.00 - 10.20', '09.00 - 10.20'),
    ('10.50 - 12.10', '10.50 - 12.10'),
    ('12.55 - 14.15', '12.55 - 14.15'),
    ('14.45 - 16.05', '14.45 - 16.05'),
)


class Discipline(models.Model):
    s_name = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    s_name = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Group(models.Model):
    s_name = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Assign(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, null=True)
    assign_view = models.CharField(choices=ASSIGN_VIEW, max_length=15, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '%s : %s : %s : %s' % (self.teacher, self.discipline, self.assign_view, self.group)


class AssignTime(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    period = models.CharField(choices=time_slots, max_length=50)
    day = models.CharField(choices=DAYS_OF_WEEK, max_length=15)
    start_date = models.DateField()
    end_date = models.DateField()


class AttendanceClass(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.IntegerField(default=2)

    def __str__(self):
        return '%s : %s : %s' % (self.assign, self.date, self.hours)


class AttendanceTotalHours(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    total_hours = models.IntegerField()

    def __str__(self):
        return '%s : %s' % (self.assign, self.total_hours)


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
        start_date = AssignTime.objects.all()[:1].get().start_date
        end_date = AssignTime.objects.all()[:1].get().end_date
        ass = Assign.objects.all()[:1]
        for single_date in daterange(start_date, end_date):
            if single_date.isoweekday() == days[instance.day]:
                try:
                    AttendanceClass.objects.get(date=single_date.strftime("%Y-%m-%d"), assign=instance.assign)
                except AttendanceClass.DoesNotExist:
                    a = AttendanceClass(date=single_date.strftime("%Y-%m-%d"), assign=instance.assign)
                    a.save()
        for i in range(len(ass)):
            AttendanceTotalHours(assign=instance.assign, total_hours=AttendanceClass.objects.filter(assign_id=ass[i].id).count()*2).save()


post_save.connect(create_attendance, sender=AssignTime)

