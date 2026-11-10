from .views import *
from django.urls import path

app_name = "Expedition"
urlpatterns = [
    path('home/', home, name='home'),
    path('w/<str:name>', welcome, name="welcomeFunction"),
    path('list/', listExpeditions, name="list"),
    path('detail/<int:id>/', detailExpedition, name="detail"), # <-- name="detail"
    path('list_expeditions/', Liste_expedition.as_view(), name='liste_expedition'),
    path('detail_expedition/<int:pk>/', Detail_expedition.as_view(), name='detail_expedition'),
    path('delete_expedition/<int:pk>/', Delete_expedition.as_view(), name='delete_expedition'),
    path('create_expedition/', CreateExpedition.as_view(), name='create_expedition'),
    path('update_expedition/<int:pk>/', UpdateExpedition.as_view(), name='update_expedition'),
]