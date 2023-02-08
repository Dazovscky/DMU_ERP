from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *
import xlwt
from .resources import *


def index(request):
    att_class = AttendanceClass.objects.all()
    template = loader.get_template('timetable/index.html')
    context = {
        'att_class': att_class,
    }
    return HttpResponse(template.render(context, request))


def total_hours(request):
    att_total = AttendanceTotalHours.objects.all()
    template = loader.get_template('timetable/total.html')
    context = {
        'att_total': att_total,
    }
    return HttpResponse(template.render(context, request))


def export_xls(request):
    if request.method == 'POST':
        comment_resource = CommentResource()
        dataset = comment_resource.export()
        response = HttpResponse(dataset.xls, content_type='timetable/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
        return response
        return render(request, 'timetable/total.html')