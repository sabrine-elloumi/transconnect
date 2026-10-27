from django.http import HttpResponse
from django.shortcuts import render
from .models import Expedition

def home(request):
    return HttpResponse("<h1> Welcome To ...</h1>")

def welcome(request, name):
    return HttpResponse(f"Hello {name}")

def listExpeditions(request):
    liste = Expedition.objects.filter(statut="publiee").order_by("date_souhaitee")
    return render(request, 'expedition/list.html', {"list": liste})

def detailExpedition(request, id):
    expedition = Expedition.objects.get(id=id)
    return render(request, 'expedition/detail.html', {"expedition": expedition})
