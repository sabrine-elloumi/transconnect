from django.db import models
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

    def save(self, *args, **kwargs):
        if not self.reference:
            last = Expedition.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.reference = f"EXP-{next_id:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} ({self.ville_depart} → {self.ville_arrivee})"