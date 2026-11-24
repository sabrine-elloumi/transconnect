from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, TemplateView, UpdateView

from .forms import ProfileUpdateForm, RegisterUserForm

User = get_user_model()


# ============================================================
# INSCRIPTION
# ============================================================
def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'offre/register_success.html')
    else:
        form = RegisterUserForm()

    return render(request, 'offre/register.html', {'form': form})


# ============================================================
# AFFICHAGE DU PROFIL
# ============================================================
class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Affiche le profil de l'utilisateur connecté.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    template_name = 'offre/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Alias explicite pour le template (bien que `user` soit déjà dispo)
        context['profile_user'] = self.request.user
        return context


# ============================================================
# MODIFICATION DU PROFIL
# ============================================================
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Permet à l'utilisateur de modifier ses propres informations.
    On force get_object() à retourner self.request.user pour
    empêcher la modification d'un autre compte (sécurité).
    """
    model = User
    form_class = ProfileUpdateForm
    template_name = 'offre/profile_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


# ============================================================
# SUPPRESSION DU COMPTE
# ============================================================
class AccountDeleteView(LoginRequiredMixin, DeleteView):
    """
    Permet à l'utilisateur de supprimer son propre compte.
    On déconnecte AVANT la suppression pour éviter une session orpheline.
    """
    model = User
    template_name = 'offre/profile_confirm_delete.html'
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        # Déconnexion propre avant suppression
        logout(self.request)
        return super().form_valid(form)