from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def app_test_hello(request):
    return HttpResponse("<h1>hello app test!</h1>")
