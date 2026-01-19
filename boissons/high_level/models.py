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
        return self.nom

    def json(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "stock": self.stock,
            "emprise": self.emprise,
        }

    def json_extended(self):
        return self.json()


class QuantiteMatierePremiere(models.Model):
    quantite = models.IntegerField()
    matiere_premiere = models.ForeignKey(
        MatierePremiere,
        on_delete=models.PROTECT,
    )

    class Meta:
        abstract = True

    def json(self):
        return {
            "id": self.id,
            "quantite": self.quantite,
            "matiere_premiere_id": self.matiere_premiere.json(),
        }


class Metier(models.Model):
    nom = models.CharField(max_length=100)
    remuneration = models.IntegerField()

    def __str__(self):
        return self.nom

    def json(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "remuneration": self.remuneration,
        }

    def json_extended(self):
        return self.json()


class Localisation(models.Model):
    nom = models.CharField(max_length=100)
    taxes = models.IntegerField()
    prix_m2 = models.IntegerField()

    def __str__(self):
        return self.nom

    def json(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "taxes": self.taxes,
            "prix_m2": self.prix_m2,
        }

    def json_extended(self):
        return {
            **self.json(),
            "energies": [e.json() for e in self.energie_set.all()],
            "locaux": [l.json() for l in self.local_set.all()],
            "approvisionnements": [a.json() for a in self.approvisionnementmatierepremiere_set.all()],
        }


class Energie(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    localisation = models.ForeignKey(
        Localisation,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.nom

    def json(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prix": self.prix,
            "localisation_id": self.localisation.json(),
        }

    def json_extended(self):
        return {
            **self.json(),
            "debits": [d.json() for d in self.debitenergie_set.all()],
        }


class DebitEnergie(models.Model):
    debit = models.IntegerField()
    energie = models.ForeignKey(
        Energie,
        on_delete=models.PROTECT,
    )

    def json(self):
        return {
            "id": self.id,
            "debit": self.debit,
            "energie_id": self.energie.json(),
        }

    def json_extended(self):
        return self.json()


class Local(models.Model):
    nom = models.CharField(max_length=100)
    localisation = models.ForeignKey(
        Localisation,
        on_delete=models.PROTECT,
    )
    surface = models.IntegerField()

    def __str__(self):
        return self.nom

    def costs(self):
        prix_m2 = self.localisation.prix_m2
        stock = MatierePremiere.objects.first().stock
        prix_unitaire = ApprovisionnementMatierePremiere.objects.first().prix_unitaire
        prix_energie = Energie.objects.first().prix
        debit_energie = DebitEnergie.objects.first().debit
        prix_machine = Machine.objects.first().prix_achat

        return (
            self.surface * prix_m2
            + stock * prix_unitaire
            + prix_energie * debit_energie
            + prix_machine
        )

    def json(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "localisation_id": self.localisation.json(),
            "surface": self.surface,
        }

    def json_extended(self):
        return {
            **self.json(),
            "produits": [p.json() for p in self.produit_set.all()],
            "machines": [m.json() for m in self.machine_set.all()],
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
        return self.nom

    def json(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prix_de_vente": self.prix_de_vente,
            "quantite": self.quantite,
            "emprise": self.emprise,
            "local_id": self.local.json(),
        }

    def json_extended(self):
        return {
            **self.json(),
            "fabrications": [f.json() for f in self.fabrication_set.all()],
        }


class UtilisationMatierePremiere(QuantiteMatierePremiere):
    def json_extended(self):
        return self.json()


class ApprovisionnementMatierePremiere(QuantiteMatierePremiere):
    localisation = models.ForeignKey(
        Localisation,
        on_delete=models.PROTECT,
    )
    prix_unitaire = models.IntegerField()
    delais = models.IntegerField()

    def json(self):
        return {
            "id": self.id,
            "localisation_id": self.localisation.json(),
            "prix_unitaire": self.prix_unitaire,
            "delais": self.delais,
        }

    def json_extended(self):
        return self.json()


class RessourceHumaine(models.Model):
    metier = models.ForeignKey(
        Metier,
        on_delete=models.PROTECT,
    )
    quantite = models.IntegerField()

    def json(self):
        return {
            "id": self.id,
            "metier_id": self.metier.json(),
            "quantite": self.quantite,
        }

    def json_extended(self):
        return self.json()


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
        return self.nom

    def json(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prix_achat": self.prix_achat,
            "cout_maintenance": self.cout_maintenance,
            "operateurs": list(self.operateurs.values_list("id", flat=True)),
            "debit": self.debit,
            "surface": self.surface,
            "debit_energie": self.debit_energie,
            "taux_utilisation": self.taux_utilisation,
            "local_id": self.local.id,
        }

    def json_extended(self):
        return {
            **self.json(),
            "operateurs_details": [o.json() for o in self.operateurs.all()],
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
        return {
            "id": self.Metierid,
            "produit_id": self.produit.json(),
            "utilisations_matiere_premiere": list(
                self.utilisations_matiere_premiere.values_list("id", flat=True)
            ),
            "machines": list(self.machines.values_list("id", flat=True)),
            "ressources_humaines": list(
                self.ressources_humaines.values_list("id", flat=True)
            ),
        }

    def json_extended(self):
        return {
            "id": self.id,
            "produit": self.produit.json(),
            "utilisations_matiere_premiere": [u.json() for u in self.utilisations_matiere_premiere.all()],
            "machines": [m.json() for m in self.machines.all()],
            "ressources_humaines": [r.json() for r in self.ressources_humaines.all()],
        }
