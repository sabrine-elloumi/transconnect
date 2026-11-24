from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'register_success.html')  # Redirect to a success page after registration
    else:
        form = RegisterUserForm()
    return render(request, 'register.html' , {'form': form })