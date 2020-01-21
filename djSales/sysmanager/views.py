from django.shortcuts import render, HttpResponse

# Create your views here.

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
