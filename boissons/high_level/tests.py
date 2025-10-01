# Create your tests here.
# high_level/tests.py
from django.test import TestCase
from .models import*
class MachineModelTests(TestCase):
    def test_cout_(self):
        self.assertEqual(Localisation.objects.count(), 0)
        l=Localisation.objects.create(nom="Toulouse",taxes=0,prix_m2=2000)
        loc=Local.objects.create(nom="usine", localisation=l,surface=50)
        eau=Energie.objects.create(nom="eau", prix=15,localisation=l)
        deb=DebitEnergie.objects.create(debit=50,energie=eau)
        m=MatierePremiere.objects.create(nom="sucre",stock=1000,emprise=20)
        ApprovisionnementMatierePremiere.objects.create(localisation=l,prix_unitaire=10,delais=12,quantite=1000,matiere_premiere=m)
        ma=Machine.objects.create(nom="laas",prix_achat=3000,cout_maintenance=0,debit=30,surface=123,debit_energie=50,taux_utilisation=0,local=loc)
        coutLOCAL= Local.objects.first().costs()


        metier=Metier.objects.create(nom="kheray", remuneration=1)

        print(eau.toJSON())
        #self.assertEqual(Localisation.objects.count(), 1)