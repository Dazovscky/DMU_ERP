from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('export/', views.export_users_xls, name='export_users_xls'),

]