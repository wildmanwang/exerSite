from django.shortcuts import render
from apps.sysmanager.views import auth

# Create your views here.


@auth
def index(request, user):
    return render(request, "blogs/index.html", {"user": user})
