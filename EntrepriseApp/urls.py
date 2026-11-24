from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),

    # Profil
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/delete/', views.AccountDeleteView.as_view(), name='profile_delete'),
]