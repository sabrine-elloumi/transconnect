from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from VehiculeApp.models import Vehicule
from .models import Utilisateur, Entreprise

#register your models here.
admin.site.site_header = 'TransConnect - Administration'
admin.site.site_title = 'TransConnect'
admin.site.index_title = "Tableau de bord"

class VehiculeInline(admin.TabularInline):
    model = Vehicule
    fields = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponible')
    extra = 2
    show_change_link = True



@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('user_id', 'username', 'email')
    ordering = ('-date_joined',)
    readonly_fields = ('user_id',)

    fieldsets = UserAdmin.fieldsets + (
        ('Informations TransConnect', {
            'fields': ('user_id', 'telephone', 'role'),
        }),
    )
    add_fieldsets = (
        
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'telephone', 'role', 'password1', 'password2' ,'usable_password'),
        }),
    )


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    inlines = [VehiculeInline]
    list_display = ('raison_sociale', 'matricule_fiscal', 'type_entreprise', 'utilisateur', 'created_at')
    list_filter = ('type_entreprise',)
    search_fields = ('raison_sociale', 'matricule_fiscal')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Informations générales', {
            'fields': ('raison_sociale', 'matricule_fiscal', 'type_entreprise')
        }),
        ('Contact et rattachement', {
            'fields': ('adresse', 'utilisateur')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )