from django.db import models
from django.core.exceptions import ValidationError
from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule
from ExpeditionApp.models import Expedition


class Offre(models.Model):
    STATUT_CHOICES = [
        ('proposee', 'Proposée'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('retiree', 'Retirée'),
    ]

    prix = models.DecimalField(max_digits=10, decimal_places=2)
    delai_jours = models.PositiveIntegerField()
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='proposee',
    )
    date_proposition = models.DateField(auto_now_add=True)

    expedition = models.ForeignKey(
        Expedition,
        on_delete=models.CASCADE,
        related_name='offres',
    )
    transporteur = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='offres_proposees',
    )
    vehicule = models.ForeignKey(
        Vehicule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='offres',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        #un transporteur ne peut proposer qu'UNE offre par expédition
        unique_together = ('expedition', 'transporteur')

    def clean(self):
        super().clean()

        #le transporteur doit être de type 'Transporteur'
        if self.transporteur and self.transporteur.type_entreprise != 't':
            raise ValidationError(
                "L'entreprise associée à l'offre doit être de type Transporteur."
            )

        #le véhicule doit appartenir au transporteur
        if self.vehicule and self.transporteur and self.vehicule.entreprise_id != self.transporteur_id:
            raise ValidationError(
                "Le véhicule doit appartenir au transporteur qui propose l'offre."
            )

        # l'expédition doit être en statut 'publiee' pour recevoir des offres
        if self.expedition and self.expedition.statut != 'publiee':
            raise ValidationError(
                "On ne peut proposer une offre que sur une expédition au statut 'publiee'."
            )

        #prix et délai positifs
        if self.prix is not None and self.prix <= 0:
            raise ValidationError("Le prix doit être strictement positif.")
        if self.delai_jours is not None and self.delai_jours <= 0:
            raise ValidationError("Le délai doit être strictement positif.")

        # un transporteur ne peut proposer qu'une offre par expédition
        if self.expedition and self.transporteur:
            doublon = (
                Offre.objects
                .filter(expedition=self.expedition, transporteur=self.transporteur)
                .exclude(pk=self.pk)
                .exists()
            )
            if doublon:
                raise ValidationError(
                    "Ce transporteur a déjà proposé une offre sur cette expédition."
                )

    def save(self, *args, **kwargs):
        self.full_clean()                       
        super().save(*args, **kwargs)

        # Règle métier 7 : quand une offre est acceptée
        if self.statut == 'acceptee':
            # 7a. L'expédition passe à 'attribuee'
            self.expedition.statut = 'attribuee'
            self.expedition.save()

            # 7b. Les autres offres sur cette expédition passent à 'refusee'
            autres_offres = (
                Offre.objects
                .filter(expedition=self.expedition)
                .exclude(pk=self.pk)
            )
            for autre in autres_offres:
                if autre.statut != 'refusee':
                    autre.statut = 'refusee'
                    autre.save()

            #Le véhicule assigné devient indisponible
            if self.vehicule:
                self.vehicule.disponible = False
                self.vehicule.save()

    def __str__(self):
        return f"Offre {self.prix} € / {self.delai_jours}j — {self.get_statut_display()}"