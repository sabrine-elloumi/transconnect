from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Expedition
from EntrepriseApp.models import Entreprise



class EnRetardFilter(admin.SimpleListFilter):
    title = "en retard"
    parameter_name = "en_retard"

    def lookups(self, request, model_admin):
        return [("oui", "Oui"), ("non", "Non")]

    def queryset(self, request, queryset):
        aujourd_hui = timezone.now().date()

        if self.value() == "oui":
            return queryset.filter(statut='publiee', date_souhaitee__lt=aujourd_hui)

        if self.value() == "non":
            return queryset.exclude(statut='publiee', date_souhaitee__lt=aujourd_hui)
            
        return queryset


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = (
        'reference',
        'ville_depart',
        'ville_arrivee',
        'poids_kg',
        'statut_colore',      
        'entreprise',
        'created_at',
    )

    list_filter = ('statut', 'date_souhaitee', 'entreprise', EnRetardFilter)
    search_fields = ('reference', 'ville_depart', 'ville_arrivee', 'description')
    readonly_fields = ('reference', 'created_at', 'updated_at')
    date_hierarchy = 'date_souhaitee'
    ordering = ('-created_at',)

    fieldsets = (
        ('Référence', {
            'fields': ('reference',)
        }),
        ('Trajet et détails', {
            'fields': ('ville_depart', 'ville_arrivee', 'poids_kg', 'date_souhaitee', 'description')
        }),
        ('Statut et rattachement', {
            'fields': ('statut_colore', 'statut', 'entreprise')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


    @admin.display(description='Statut')
    def statut_colore(self, obj):
        couleurs = {
            'publiee': '#0D6EFD',   
            'attribuee': '#F0AD4E', 
            'en_cours': '#17A2B8',  
            'livree': '#5CB85C',   
            'annulee': '#D9534F',   
        }
        return format_html(
            '<span style="color:white;background:{};padding:3px 8px;border-radius:4px;">{}</span>',
            couleurs.get(obj.statut, '#999'),
            obj.get_statut_display(),
        )


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "entreprise":
            kwargs["queryset"] = Entreprise.objects.filter(type_entreprise='c')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)