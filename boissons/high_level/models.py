from django.db import models

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
    def json(self):
        return{
            'id': self.id,
            'nom': self.nom,
            'stock': self.stock,
            'emprise': self.emprise,
        }


class QuantiteMatierePremiere(models.Model):
    quantite = models.IntegerField()
    matiere_premiere = models.ForeignKey(
        MatierePremiere,
        on_delete=models.PROTECT,
    )

    class Meta:
        abstract = True
    def json(self):
        return{
            'id': self.id,
            'quantite': self.quantite,
            'matiere_premiere_id': self.matiere_premiere.json(),
        }

class Metier(models.Model):
    nom = models.CharField(max_length=100)
    remuneration = models.IntegerField()
    def __str__(self):
        return(self.nom)
    def json(self):
        return{
            'id': self.id,
            'nom': self.nom,
            'remuneration': self.remuneration,
        }

class Localisation(models.Model):
    nom = models.CharField(max_length=100)
    taxes = models.IntegerField()
    prix_m2 = models.IntegerField()
    def __str__(self):
        return(self.nom)
    def json(self):
        return{
            'id': self.id,
            'nom': self.nom,
            'taxes': self.taxes,
            'prix_m2': self.prix_m2,
        }


class Energie(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    localisation = models.ForeignKey(
        Localisation,
        on_delete=models.PROTECT,
    )
    def __str__(self):
        return(self.nom)
    def json(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prix': self.prix,
            'localisation_id': self.localisation.json(),
        }

class DebitEnergie(models.Model):
    debit = models.IntegerField()
    energie = models.ForeignKey(
        Energie,
        on_delete=models.PROTECT,
    )
    def json(self):
        return {
            'id': self.id,
            'debit': self.debit,
            'energie_id': self.energie.json(),
        }
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
    def json(self):
        return{
            'id': self.id,
            'nom': self.nom,
            'localisation_id': self.localisation.json(),
            'surface': self.surface,
        }

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
    def json(self):
        return{
            'id': self.id,
            'nom': self.nom,
            'prix_de_vente': self.prix_de_vente,
            'quantite': self.quantite,
            'emprise': self.emprise,
            'local_id': self.local.json(),
        }

class UtilisationMatierePremiere(QuantiteMatierePremiere):
    pass


class ApprovisionnementMatierePremiere(QuantiteMatierePremiere):
    localisation = models.ForeignKey(
        Localisation,
        on_delete=models.PROTECT,
    )
    prix_unitaire = models.IntegerField()
    delais = models.IntegerField()
    def json(self):
        return{
            'id': self.id,
            'localisation_id': self.Localisation.json(),
            'prix_unitaire': self.prix_unitaire,
            'delais': self.delais,
        }

class RessourceHumaine(models.Model):
    metier = models.ForeignKey(
        Metier,
        on_delete=models.PROTECT,
    )
    quantite = models.IntegerField()
    def json(self):
        return{
            'id': self.id,
            'metier_id': self.metier.json(),
            'quantite': self.quantite,
        }


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
    def json(self):
        return{
            'id': self.id,
            'prix_achat': self.prix_achat,
            'cout_maintenance': self.cout_maintenance,
            'operateurs': list(self.operateurs.valuer_liste('id', falt=True)),
            'surface': self.surface,
            'debit_energie_id': self.debit_energie.json(),
            'taux_utilisation': self.taux_utilisation,
            'local_id': self.local.id,
        }

class Fabrication(models.Model):
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
    )
    utilisations_matiere_premiere = models.ManyToManyField(UtilisationMatierePremiere)
    machines = models.ManyToManyField(Machine)
    ressources_humaines = models.ManyToManyField(RessourceHumaine)
    def json(self):
        return{
            'id': self.Metierid,
            'produit_id': self.produit.json(),
            'utilisations_matiere_premiere': list(self.utilisations_matiere_premiere.valuer_liste('id', falt=True)),
            'machines': list(self.machines.valuer_liste('id', falt=True)),
            'ressources_humaines': list(self.ressources_humaines.valuer_liste('id', falt=True)),
        }