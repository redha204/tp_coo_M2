
from django.views.generic import DetailView
from django.http import JsonResponse 
from django.http import HttpResponse
from .models import *
class JsonDetailView(DetailView):
    def render_to_response(self, context, **response_kwargs):
        obj = self.get_object()
        if not hasattr(obj, 'toJSON'):
            return HttpResponse({
                'error': f'{obj.__class__.__name__} n\'a pas de méthode json()'
            }, status=500)
        
        try:
            return HttpResponse(obj.toJSON(),content_type='application/json')
        except Exception as e:
            return HttpResponse({
                'error': f'Erreur lors de la sérialisation: {str(e)}'
            }, status=500)
class QuantiteMatierePremiereDetailView(JsonDetailView):
    model = QuantiteMatierePremiere
class MatierePremiereDetailView(JsonDetailView):
    model = MatierePremiere
class MetierDetailView(JsonDetailView):
    model = Metier
class LocalisationDetailView(JsonDetailView):
    model = Localisation
class EnergieDetailView(JsonDetailView):
    model = Energie
class DebitEnergieDetailView(JsonDetailView):
    model = DebitEnergie
class LocalDetailView(JsonDetailView):
    model = Local
class ProduitDetailView(JsonDetailView):
    model = Produit
class UtilisationMatierePremiereDetailView(JsonDetailView):
    model = UtilisationMatierePremiere
class ApprovisionnementMatierePremiereDetailView(JsonDetailView):
    model = ApprovisionnementMatierePremiere
class RessourceHumaineDetailView(JsonDetailView):
    model = RessourceHumaine
class MachineDetailView(JsonDetailView):
    model = Machine
class FabricationDetailView(JsonDetailView):
    model = Fabrication
     