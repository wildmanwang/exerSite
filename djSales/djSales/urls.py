"""djSales URL Configuration

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
import sysmanager.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', sysmanager.views.login),
    path('myDesk', sysmanager.views.myDesk),
    re_path('products-(?P<pageNo>\d+)', sysmanager.views.products),
    re_path('products-new$', sysmanager.views.products_new),
    re_path('products-modify-(?P<recid>\d+)', sysmanager.views.products_modify),
    re_path('products-detail-(?P<recid>\d+)', sysmanager.views.products_detail),
    re_path('products-delete-(?P<recid>\d+)', sysmanager.views.products_delete),
    re_path('customers-(?P<pageNo>\d+)', sysmanager.views.customers),
    re_path('customers-new$', sysmanager.views.customers_new),
    re_path('customers-modify-(?P<recid>\d+)', sysmanager.views.customers_modify),
    re_path('customers-detail-(?P<recid>\d+)', sysmanager.views.customers_detail),
    re_path('customers-delete-(?P<recid>\d+)', sysmanager.views.customers_delete),
    re_path('cusEmployees-(?P<pageNo>\d+)', sysmanager.views.cusEmployees),
    re_path('cusEmployees-new$', sysmanager.views.cusEmployees_new),
    re_path('cusEmployees-modify-(?P<recid>\d+)', sysmanager.views.cusEmployees_modify),
    re_path('cusEmployees-detail-(?P<recid>\d+)', sysmanager.views.cusEmployees_detail),
    re_path('cusEmployees-delete-(?P<recid>\d+)', sysmanager.views.cusEmployees_delete),
]
