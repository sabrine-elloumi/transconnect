from django import forms
from .models import Expedition




from django import forms
from .models import Expedition

class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = Expedition
        fields = ['ville_depart', 'ville_arrivee', 'poids_kg', 'date_souhaitee', 'description', 'entreprise']