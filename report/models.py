from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save

DAYS_OF_WEEK = (
    ('Понеділок', 'Понеділок'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)

ASSIGN_VIEW = (
    ('Лекція', 'Лекція'),
    ('Практика', 'Практика')
)

time_slots = (
    ('09.00 - 10.20', '09.00 - 10.20'),
    ('10.50 - 12.10', '10.50 - 12.10'),
    ('12.55 - 14.15', '12.55 - 14.15'),
    ('14.45 - 16.05', '14.45 - 16.05'),
)


class Teacher(models.Model):
    s_name = models.CharField(max_length=20, verbose_name="Им'я")
    name = models.CharField(max_length=100, verbose_name="ФИО")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Викладачі'
        verbose_name_plural = 'Викладачі'


class Discipline(models.Model):
    s_name = models.CharField(max_length=20, verbose_name="Коротка назва")
    name = models.CharField(max_length=100, verbose_name="Повна назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дисципліни'
        verbose_name_plural = 'Дисципліни'


class Course(models.Model):
    course = models.IntegerField(verbose_name="Курс")
    group_name = models.CharField(max_length=100, verbose_name="Группа")

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = 'Групи'
        verbose_name_plural = 'Групи'


class Assign(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, null=True, verbose_name="Дисципліна")
    assign_view = models.CharField(choices=ASSIGN_VIEW, max_length=15, null=True, verbose_name="Вид заняття")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, verbose_name="Викладач")
    group = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, verbose_name="Група")
    hours = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return '%s : %s : %s : %s' % (self.teacher, self.discipline, self.assign_view, self.group)

    class Meta:
        verbose_name = 'Заняття'
        verbose_name_plural = 'Заняття'


class AssignTime(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    period = models.CharField(choices=time_slots, max_length=50)
    day = models.CharField(choices=DAYS_OF_WEEK, max_length=15)
    hour = models.IntegerField(default=2)

    class Meta:
        verbose_name = 'подію'
        verbose_name_plural = 'події'


class AttendanceClass(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE, verbose_name="Заняття", null=True)
    #teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Викладач")
    date = models.DateField(verbose_name="Дата проведення")
    hours = models.IntegerField(blank=True, verbose_name="Годин проведено", null=True)

    def __str__(self):
        return '%s : %s : %s' % (self.assign, self.date, self.hours)

    class Meta:
        verbose_name = 'Події'
        verbose_name_plural = 'Події'


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


days = {
    'Понеділок': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
}


def create_attendance(sender, instance, **kwargs):
    if kwargs['created']:
        start_date = Assign.objects.all()[:1].get().start_date
        end_date = Assign.objects.all()[:1].get().end_date
        for single_date in daterange(start_date, end_date):
            if single_date.isoweekday() == days[instance.day]:
                try:
                    AttendanceClass.objects.get(date=single_date.strftime("%Y-%m-%d"), assign=instance.assign)
                except AttendanceClass.DoesNotExist:
                    a = AttendanceClass(date=single_date.strftime("%Y-%m-%d"), assign=instance.assign)
                    a.save()


def total(sender, instance, **kwargs):
    if kwargs['created']:
        assign_time = AssignTime.objects.all()
        list_hours = []
        for id in assign_time:
            list_hours.append(id.hour)
            print(list_hours)
        Assign.objects.update(hours=sum(list_hours))


def delete(sender, instance, **kwargs):
    assign_time = AssignTime.objects.all()
    list_hours = []
    for id in assign_time:
        list_hours.append(id.hour)
    Assign.objects.update(hours=sum(list_hours))


def update(sender, *args, **kwargs):
    assign_time = AssignTime.objects.all()
    list_hours = []
    for id in assign_time:
        list_hours.append(id.hour)
        print(id.hour)
        print(list_hours)
    Assign.objects.update(hours=sum(list_hours))


post_save.connect(total, sender=AssignTime)
post_save.connect(update, sender=AssignTime)
post_delete.connect(delete, sender=AssignTime)
post_save.connect(create_attendance, sender=AssignTime)