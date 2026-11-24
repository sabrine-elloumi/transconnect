from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


# ============================================================
# FORMULAIRE D'INSCRIPTION
# ============================================================
class RegisterUserForm(UserCreationForm):
    """
    Formulaire d'inscription basé sur le modèle Utilisateur.
    
    ⚠️ Si tu avais DÉJÀ un RegisterUserForm dans ce fichier, garde-le
    et ajoute seulement la classe ProfileUpdateForm plus bas.
    Sinon, ce formulaire fonctionne avec un Utilisateur qui hérite
    d'AbstractUser (username, email, first_name, last_name, ...).
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text="Une adresse email valide.",
    )

    class Meta:
        model = User
        # ⚠️ ADAPTE cette liste selon les champs de ton modèle Utilisateur
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Un compte avec cet email existe déjà.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# ============================================================
# FORMULAIRE DE MODIFICATION DU PROFIL
# ============================================================
class ProfileUpdateForm(forms.ModelForm):
    """
    Permet à l'utilisateur de modifier ses propres informations
    (sans toucher au mot de passe, géré par le formulaire d'admin).
    """
    class Meta:
        model = User
        # ⚠️ ADAPTE cette liste selon les champs de ton modèle Utilisateur
        #    Champs typiques : username, email, first_name, last_name,
        #    telephone, adresse, ville, ...
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # On exclut l'utilisateur courant pour ne pas le bloquer sur son propre email
            qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Cet email est déjà utilisé par un autre compte.")
        return email