import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


# VALIDATEURS


user_id_validator = RegexValidator(
    regex=r'^\d{2}user\d{2}$',
    message="Format attendu : AAuserNN (ex: 26user00)"
)

matricule_fiscal_validator = RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
    message="Format de matricule fiscal invalide. Exemple : 1234567A/B/M/123"
)

adresse_validators = [
    MinLengthValidator(20, "L'adresse ne peut pas avoir moins de 20 caractères."),
    MaxLengthValidator(400, "L'adresse ne peut pas avoir plus de 400 caractères."),
]


# Utilisateur


class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('c', 'Chargeur'),
        ('t', 'Transporteur'),
    ]

    user_id = models.CharField(
        primary_key=True,
        max_length=8,
        validators=[user_id_validator],
        editable=False,
    )
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='c')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def _generate_user_id(cls):
        """Génère un user_id au format AAuserNN (AA = année, NN = compteur)."""
        annee = timezone.now().strftime('%y')          # '26'
        prefix = f"{annee}user"                        # '26user'
        dernier = (
            cls.objects
            .filter(user_id__startswith=prefix)
            .order_by('user_id')
            .last()
        )
        if dernier:
            try:
                num = int(dernier.user_id[-2:]) + 1
            except (ValueError, IndexError):
                num = 0
        else:
            num = 0
        return f"{prefix}{num:02d}"                    # '26user00'

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self._generate_user_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


# Entreprise


class Entreprise(models.Model):
    TYPE_CHOICES = [
        ('c', 'Chargeur'),
        ('t', 'Transporteur'),
    ]

    raison_sociale = models.CharField(max_length=200)
    matricule_fiscal = models.CharField(
        max_length=25,
        unique=True,
        validators=[matricule_fiscal_validator],
    )
    adresse = models.TextField(validators=adresse_validators)
    type_entreprise = models.CharField(max_length=1, choices=TYPE_CHOICES)

    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='entreprise',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        # Le rôle de l'utilisateur doit correspondre au type d'entreprise
        if self.utilisateur and self.type_entreprise:
            role_attendu = self.type_entreprise
            if self.utilisateur.role not in (role_attendu, 'admin'):
                raise ValidationError(
                    "Le rôle de l'utilisateur ne correspond pas au type d'entreprise."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.raison_sociale