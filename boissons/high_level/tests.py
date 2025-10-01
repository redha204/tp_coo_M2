# Create your tests here.
# high_level/tests.py
from django.test import TestCase
from .models import (
    Localisation,
    Local,
    Energie,
    DebitEnergie,
    Machine,
    MatierePremiere,
    ApprovisionnementMatierePremiere,
)


class MachineModelTests(TestCase):
    def test_cout_(self):
        self.assertEqual(Localisation.objects.count(), 0)
        l = Localisation.objects.create(nom="malaga", taxes=0, prix_m2=2000)
        loc = Local.objects.create(nom="usine", localisation=l, surface=50)
        eau1 = Energie.objects.create(nom="eau", prix=15, localisation=l)
        deb = DebitEnergie.objects.create(debit=50, energie=eau1)
        m = MatierePremiere.objects.create(nom="sucre", stock=1000, emprise=20)
        ApprovisionnementMatierePremiere.objects.create(
            localisation=l,
            prix_unitaire=10,
            delais=12,
            quantite=1000,
            matiere_premiere=m,
        )
        Machine.objects.create(
            nom="laas",
            prix_achat=3000,
            cout_maintenance=0,
            debit=30,
            surface=123,
            debit_energie=50,
            taux_utilisation=0,
            local=loc,
        )
        MatierePremiere.objects.create(nom="sucre", stock=1000, emprise=20)

        cout = Local.objects.first().costs()
        print(cout)
        print(eau1.json())
        print(l.json())
        print(loc.json())
        print(deb.json())
