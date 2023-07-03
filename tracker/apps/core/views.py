from django.shortcuts import render
from django.http import HttpResponse


# to be removed (testing)
def dashboard(request):
    return HttpResponse("Welcome to the Dashboard")
