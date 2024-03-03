from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import redirect
from django.urls import reverse


def index(request):
    return render(request, 'blink/index.html')
