import django.contrib.auth.forms as auth_forms
from django import forms
from .models import Utilisateur



auth_forms.UserCreationForm
class RegisterUserForm(auth_forms.UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(auth_forms.UserCreationForm.Meta):
        model = Utilisateur
        fields = auth_forms.UserCreationForm.Meta.fields + ("first_name", "last_name", "email")

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user