from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from EntrepriseApp.models import Entreprise


class Vehicule(models.Model):
    TYPE_CHOICES = [
        ('camionnette', 'Camionnette'),
        ('fourgon', 'Fourgon'),
        ('camion_porteur', 'Camion porteur'),
        ('semi_remorque', 'Semi-remorque'),
    ]

    immatriculation = models.CharField(max_length=20, unique=True)
    type_vehicule = models.CharField(max_length=20, choices=TYPE_CHOICES)
    capacite_kg = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, "La capacité doit être supérieure à 0 kg"),
            MaxValueValidator(10000, "La capacité ne peut pas dépasser 10000 kg"),
        ]
    )
    disponible = models.BooleanField(default=True)

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='vehicules',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        # Règle métier : un véhicule appartient à une entreprise TRANSPORTEUR
        if self.entreprise and self.entreprise.type_entreprise != 't':
            raise ValidationError(
                "Un véhicule ne peut être rattaché qu'à une entreprise de type Transporteur."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.immatriculation} ({self.get_type_vehicule_display()})"