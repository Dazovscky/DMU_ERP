from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import *


class AssignTimeInline(admin.TabularInline):
    model = AssignTime
    extra = 0


class AssignAdmin(admin.ModelAdmin):
    inlines = [AssignTimeInline]



admin.site.register(Teacher)
admin.site.register(Discipline)
admin.site.register(Group)
admin.site.register(Assign, AssignAdmin)
admin.site.register(AttendanceClass)