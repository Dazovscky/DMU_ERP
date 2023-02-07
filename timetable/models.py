from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig
from django.db import models
from django.db.models.signals import post_save


class MyAppConfig(AppConfig):
    name = 'Timetable'
    verbose_name = _('Transalation of MyApp here')


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


class Discipline(models.Model):
    s_name = models.CharField(max_length=20, verbose_name="Коротка назва")
    name = models.CharField(max_length=100, verbose_name="Повна назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дисципліни'
        verbose_name_plural = 'Дисципліни'


class Teacher(models.Model):
    s_name = models.CharField(max_length=20, verbose_name="Им'я")
    name = models.CharField(max_length=100, verbose_name="ФИО")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Викладачі'
        verbose_name_plural = 'Викладачі'


class Group(models.Model):
    s_name = models.CharField(max_length=20, verbose_name="Курс")
    name = models.CharField(max_length=100, verbose_name="Группа")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Групи'
        verbose_name_plural = 'Групи'


class Assign(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, null=True, verbose_name="Дисципліна")
    assign_view = models.CharField(choices=ASSIGN_VIEW, max_length=15, null=True, verbose_name="Вид заняття")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, verbose_name="Викладач")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, verbose_name="Група")

    def __str__(self):
        return '%s : %s : %s : %s' % (self.teacher, self.discipline, self.assign_view, self.group)

    class Meta:
        verbose_name = 'Заняття'
        verbose_name_plural = 'Заняття'


class AssignTime(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    period = models.CharField(choices=time_slots, max_length=50)
    day = models.CharField(choices=DAYS_OF_WEEK, max_length=15)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = 'подію'
        verbose_name_plural = 'події'


class AttendanceClass(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE, verbose_name="Заняття")
    date = models.DateField(verbose_name="Дата проведення")
    hours = models.IntegerField(default=2, verbose_name="Годин проведено")

    def __str__(self):
        return '%s : %s : %s' % (self.assign, self.date, self.hours)

    class Meta:
        verbose_name = 'Події'
        verbose_name_plural = 'Події'


class AttendanceTotalHours(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE, verbose_name="Заняття")
    total_hours = models.IntegerField(verbose_name="Години")

    def __str__(self):
        return '%s : %s' % (self.assign, self.total_hours)

    class Meta:
        verbose_name = 'Загальна кількість годин'
        verbose_name_plural = 'Загальна кількість годин'


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

