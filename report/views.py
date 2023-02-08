from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.template import loader


def index(request):
    att_class = AttendanceClass.objects.all()
    template = loader.get_template('report/base.html')
    context = {
        'att_class': att_class,
    }
    return HttpResponse(template.render(context, request))


def report(request):
    template = loader.get_template('report/report.html')
    return render(request, 'report/report.html')