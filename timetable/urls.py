from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('total/', views.total_hours, name='total'),
    path('export/xls/', views.export_xls, name='export_xls'),
]