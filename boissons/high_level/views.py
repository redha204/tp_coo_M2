# Create your views here.

from django.views.generic import DetailView
from django.http import JsonResponse
from django.views import View
from .models import *


class JsonDetailView(DetailView):
    def render_to_response(self, context, **response_kwargs):
        obj = self.get_object()
        if not hasattr(obj, "json"):
            return JsonResponse(
                {"error": f"{obj.__class__.__name__} n'a pas de méthode json()"},
                status=500,
            )

        try:
            return JsonResponse(obj.json())
        except Exception as e:
            return JsonResponse(
                {"error": f"Erreur lors de la sérialisation: {str(e)}"}, status=500
            )


class ApiView(View):
    model_mapping = {
        "matiere-premiere": MatierePremiere,
        "metier": Metier,
        "localisation": Localisation,
        "energie": Energie,
        "debit-energie": DebitEnergie,
        "local": Local,
        "produit": Produit,
        "utilisation-matiere-premiere": UtilisationMatierePremiere,
        "approvisionnement-matiere-premiere": ApprovisionnementMatierePremiere,
        "ressource-humaine": RessourceHumaine,
        "machine": Machine,
        "fabrication": Fabrication,
    }

    def get(self, request, model_name, pk):
        model_class = self.model_mapping.get(model_name)
        if not model_class:
            return JsonResponse({"error": f"Modèle '{model_name}' inconnu"}, status=404)

        try:
            obj = model_class.objects.get(pk=pk)
            if not hasattr(obj, "json_extended"):
                return JsonResponse(
                    {"error": f"{model_class.__name__} n'a pas de méthode json_extended()"},
                    status=500,
                )
            return JsonResponse(obj.json_extended())
        except model_class.DoesNotExist:
            return JsonResponse(
                {"error": f"{model_class.__name__} avec id {pk} introuvable"},
                status=404,
            )
        except Exception as e:
            return JsonResponse(
                {"error": f"Erreur: {str(e)}"}, status=500
            )


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
