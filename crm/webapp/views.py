from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    # return HttpResponse("hi")
    return render(request , 'webapp/index.html')