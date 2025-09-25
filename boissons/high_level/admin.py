# Register your models here.
from django.contrib import admin
from .models import (
    MatierePremiere, QuantiteMatierePremiere, Metier, Localisation, Energie,
    DebitEnergie, Local, Produit, UtilisationMatierePremiere,
    ApprovisionnementMatierePremiere, RessourceHumaine, Machine, Fabrication
)

admin.site.register(MatierePremiere)
admin.site.register(Metier)
admin.site.register(Localisation)
admin.site.register(Energie)
admin.site.register(DebitEnergie)
admin.site.register(Local)
admin.site.register(Produit)
admin.site.register(UtilisationMatierePremiere)
admin.site.register(ApprovisionnementMatierePremiere)
admin.site.register(RessourceHumaine)
admin.site.register(Machine)
admin.site.register(Fabrication)
