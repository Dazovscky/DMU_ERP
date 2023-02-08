from django.contrib import admin
from .models import *


class AssignPeriodInline(admin.TabularInline):
    model = AssignTime
    extra = 0


class AssignPeriod(admin.ModelAdmin):
    inlines = [AssignPeriodInline]
    list_display = ('discipline', 'assign_view', 'teacher', 'group')


class AttendanceClassAdmin(admin.ModelAdmin):
    list_display = ('assign', 'date')


admin.site.register(Discipline)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Assign, AssignPeriod)
admin.site.register(AttendanceClass, AttendanceClassAdmin)

