from datetime import datetime

from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import *
from django.urls import path


class AssignPeriodInline(admin.TabularInline):
    model = AssignTime
    extra = 0


class AssignPeriod(admin.ModelAdmin):
    inlines = [AssignPeriodInline]
    list_display = ('discipline', 'assign_view', 'teacher', 'group')


class AttendanceClassAdmin(admin.ModelAdmin):
    list_display = ('assign', 'date')


class AttendanceTotalHoursAdmin(admin.ModelAdmin):
    list_display = ('assign', 'total_hours')


admin.site.register(Discipline)
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(Assign, AssignPeriod)
admin.site.register(AttendanceClass, AttendanceClassAdmin)
admin.site.register(AttendanceTotalHours, AttendanceTotalHoursAdmin)