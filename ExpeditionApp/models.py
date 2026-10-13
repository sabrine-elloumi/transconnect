from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from EntrepriseApp.models import Entreprise


class Expedition(models.Model):
    STATUT_CHOICES = [
        ('publiee', 'Publiée'),
        ('attribuee', 'Attribuée'),
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]

    reference = models.CharField(max_length=20, unique=True, editable=False)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.DecimalField(max_digits=10, decimal_places=2)
    date_souhaitee = models.DateField()
    description = models.TextField(blank=True, null=True)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='publiee',
    )

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='expeditions',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def _generate_reference(cls):
        """Génère une référence EXP-AA-NNNNN."""
        annee = timezone.now().strftime('%y')        
        prefix = f"EXP-{annee}-"

        dernier = (
            cls.objects
            .filter(reference__startswith=prefix)
            .order_by('reference')
            .last()
        )

        if dernier:
            try:
                num = int(dernier.reference.split('-')[-1]) + 1
            except (ValueError, IndexError):
                num = 1
        else:
            num = 1

        return f"{prefix}{num:05d}"                    

    def clean(self):
        super().clean()
        # Règle métier : l'entreprise doit être de type CHARGEUR
        if self.entreprise and self.entreprise.type_entreprise != 'c':
            raise ValidationError(
                "Une expédition ne peut être créée que par une entreprise de type Chargeur."
            )
        # Règle métier : poids positif
        if self.poids_kg is not None and self.poids_kg <= 0:
            raise ValidationError("Le poids doit être strictement positif.")
        # Règle métier : date souhaitée ne peut pas être dans le passé
        if self.date_souhaitee and self.date_souhaitee < timezone.now().date():
            raise ValidationError("La date souhaitée ne peut pas être dans le passé.")

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_reference()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} ({self.ville_depart} → {self.ville_arrivee})"