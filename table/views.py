from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import xlwt


def index(request):
    assign = AssignTime.objects.all()
    attendance = AttendanceClass.objects.all()
    att_list = []
    for b in attendance:
        att_list.append(b)
    for i in assign:
        att_list.append(i)
    context = {
        'att_list': att_list,
        'assign': assign
    }
    return render(request, 'table/base.html', context)


def export_users_xls(request):
    response = HttpResponse(content_type='table/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Teacher', 'Date', 'Discipline', 'time', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = AttendanceClass.objects.get( )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
