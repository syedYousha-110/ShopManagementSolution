from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect , HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("Inventory Management")