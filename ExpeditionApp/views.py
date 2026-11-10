from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Expedition
from django.views.generic import CreateView
from django.views.generic import DetailView, ListView, DeleteView
from .forms import ExpeditionForm
from django.views.generic.edit import UpdateView


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

def deleteExpedition(request, id):
    expedition = Expedition.objects.get(id=id)
    expedition.delete()
    return HttpResponse(f"Expedition with id {id} has been deleted.")

class Liste_expedition(ListView) : 
    model=Expedition
    template_name='expedition/list.html'
    context_object_name='list'

class Detail_expedition(DetailView) :
    model=Expedition
    template_name='expedition/detail.html'
    context_object_name='expedition'

class Delete_expedition(DeleteView) :
    model=Expedition
    template_name='expedition/delete.html'
    success_url=reverse_lazy('Expedition:liste_expedition')


class CreateExpedition(CreateView):
    model = Expedition
    template_name = 'expedition/forms.html'

    form_class = ExpeditionForm 
    success_url = reverse_lazy('Expedition:liste_expedition')

class UpdateExpedition(UpdateView):
    model = Expedition
    template_name = 'expedition/forms.html'
    form_class = ExpeditionForm
    success_url = reverse_lazy('Expedition:liste_expedition')
