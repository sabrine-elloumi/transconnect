from .views import *
from django.urls import path

app_name = "Expedition"
urlpatterns = [
    path('home/', home, name='home'),
    path('w/<str:name>', welcome , name="welcomeFunction"),
    path('list/', listExpeditions, name="list"),
    path('detail/<int:id>/', detailExpedition, name='details'),
]