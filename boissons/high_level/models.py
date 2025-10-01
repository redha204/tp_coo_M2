from django.db import models
import json
# Create your models here.
# models.IntegerField()
# models.CharField(max_length=100)
# models.ManyToManyField(Machine)
# models.ForeignKey(
# Local, on_delete=models.PROTECT,
# blank=True, null=True, related_name="+",
# )


class MatierePremiere(models.Model):
    nom = models.CharField(max_length=100)
    stock = models.IntegerField()
    emprise = models.IntegerField()

    def __str__(self):
        return(self.nom)
    def toJSON(self):
        return(json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
        )
    def toJSON(self):
        return(json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
        )
    


class QuantiteMatierePremiere(models.Model):
    quantite = models.IntegerField()
    matiere_premiere = models.ForeignKey(
        MatierePremiere,
        on_delete=models.PROTECT,
    )

    class Meta:
        abstract = True
    def toJSON(self):
        return(json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
        )

class Metier(models.Model):
    nom = models.CharField(max_length=100)
    remuneration = models.IntegerField()
    def __str__(self):
        return(self.nom)
    def toJSON(self):
        return(json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
        )

class Localisation(models.Model):
    nom = models.CharField(max_length=100)
    taxes = models.IntegerField()
    prix_m2 = models.IntegerField()
    def __str__(self):
        return(self.nom)
    def toJSON(self):
        return(json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
        )

class Energie(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    localisation = models.ForeignKey(
        Localisation,
        on_delete=models.PROTECT,
    )
    def __str__(self):
        return(self.nom)
    def toJSON(self):
        return(json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
        )
class DebitEnergie(models.Model):
    debit = models.IntegerField()
    energie = models.ForeignKey(
        Energie,
        on_delete=models.PROTECT,
    )
    def toJSON(self):
        return(json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
        )

class Local(models.Model):
    nom = models.CharField(max_length=100)
    localisation = models.ForeignKey(
        Localisation,
        on_delete=models.PROTECT,
    )
    surface = models.IntegerField()
    def __str__(self):
        return(self.nom)
    def costs(self):
   
        prix_m2 = self.localisation.prix_m2
        
       
        stock = MatierePremiere.objects.first().stock
        prix_unitaire = ApprovisionnementMatierePremiere.objects.first().prix_unitaire
        prix_energie = Energie.objects.first().prix
        debit_energie = DebitEnergie.objects.first().debit
        prix_machine = Machine.objects.first().prix_achat
        
        return (
            self.surface * prix_m2 +
            stock * prix_unitaire +
            prix_energie * debit_energie +
            prix_machine
        )
    def toJSON(self):
        return(json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
        )
class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix_de_vente = models.IntegerField()
    quantite = models.IntegerField()
    emprise = models.IntegerField()
    local = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
    )
    def __str__(self):
        return(self.nom)
    def toJSON(self):
        return(json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
        )

class UtilisationMatierePremiere(QuantiteMatierePremiere):
    pass


class ApprovisionnementMatierePremiere(QuantiteMatierePremiere):
    localisation = models.ForeignKey(
        Localisation,
        on_delete=models.PROTECT,
    )
    prix_unitaire = models.IntegerField()
    delais = models.IntegerField()
    def toJSON(self):
        return(json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
        )

class RessourceHumaine(models.Model):
    metier = models.ForeignKey(
        Metier,
        on_delete=models.PROTECT,
    )
    quantite = models.IntegerField()
    def toJSON(self):
        return(json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
        )


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix_achat = models.IntegerField()
    cout_maintenance = models.IntegerField()
    operateurs = models.ManyToManyField(Metier)
    debit = models.IntegerField()
    surface = models.IntegerField()
    debit_energie = models.IntegerField()
    taux_utilisation = models.IntegerField()
    local = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
    )
    def __str__(self):
        return(self.nom)
    def toJSON(self):
        return(json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
        )

class Fabrication(models.Model):
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
    )
    utilisations_matiere_premiere = models.ManyToManyField(UtilisationMatierePremiere)
    machines = models.ManyToManyField(Machine)
    ressources_humaines = models.ManyToManyField(RessourceHumaine)
    def toJSON(self):
        return(json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
        )
