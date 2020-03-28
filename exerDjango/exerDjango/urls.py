"""exerDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
import appSys.views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('employees', appSys.views.employees, name="employees"),
    path('employeesAllInOne', appSys.views.employeesAllInOne, name="employeesAllInOne"),
    re_path('employee/detail-(?P<userID>\d+)', appSys.views.employeeDetail, name="employeeDetail"),
    path('employee/new', appSys.views.employeeNew, name="employeeNew"),
    path('employee/newmany', appSys.views.employeeNewmany, name="employeeNewmany"),
    re_path('employee/update-(?P<userID>\d+)', appSys.views.employeeUpdate, name="employeeUpdate"),
    re_path('employee/updatemany-(?P<userID>\d+)$', appSys.views.employeeUpdatemany, name="employeeUpdatemany"),
    path('employee/delete', appSys.views.employeeDelete, name="employeeDelete"),
    path('employee/deletemany', appSys.views.employeeDeletemany, name="employeeDeletemany"),

    re_path('multipages-(?P<pageNo>\d+)$', appSys.views.multipages, name="multipages"),
    re_path('uploadfile', appSys.views.uploadfile, name="uploadfile"),
    re_path("mykindeditor", appSys.views.mykindeditor, name="mykindeditor"),

    path("", appSys.views.index, name="index"),
]
