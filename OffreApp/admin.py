from django.contrib import admin
from .models import Offre

class PrixFilter(admin.SimpleListFilter):
    title = "tranche de prix"
    parameter_name = "tranche_prix"

    def lookups(self, request, model_admin):
        return [
            ("bas", "Moins de 100 €"),
            ("moyen", "Entre 100 € et 1000 €"),
            ("eleve", "Plus de 1000 €"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "bas":
            return queryset.filter(prix__lt=100)
        if self.value() == "moyen":
            return queryset.filter(prix__gte=100, prix__lte=1000)
        if self.value() == "eleve":
            return queryset.filter(prix__gt=1000)
        return queryset


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'expedition',
        'transporteur',
        'prix',
        'delai_jours',
        'statut',
        'date_proposition',
    )
    list_filter = ('statut', 'date_proposition', 'transporteur', PrixFilter)
    search_fields = ('expedition__reference', 'transporteur__raison_sociale')
    readonly_fields = ('date_proposition', 'created_at', 'updated_at')
    date_hierarchy = 'date_proposition'

    fieldsets = (
        ('Détails de l\'offre', {
            'fields': ('prix', 'delai_jours', 'statut')
        }),
        ('Relations', {
            'fields': ('expedition', 'transporteur', 'vehicule')
        }),
        ('Horodatage', {
            'fields': ('date_proposition', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )