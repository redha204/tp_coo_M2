"""
URL configuration for boissons project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from high_level import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/quantite-matiere-premiere/<int:pk>/', views.QuantiteMatierePremiereDetailView.as_view(), name='quantite-matiere-premiere-detail'),
    path('api/matiere-premiere/<int:pk>/', views.MatierePremiereDetailView.as_view(), name='matiere-premiere-detail'),
    path('api/metier/<int:pk>/', views.MetierDetailView.as_view(), name='metier-detail'),
    path('api/localisation/<int:pk>/', views.LocalisationDetailView.as_view(), name='localisation-detail'),
    path('api/energie/<int:pk>/', views.EnergieDetailView.as_view(), name='energie-detail'),
    path('api/debit-energie/<int:pk>/', views.DebitEnergieDetailView.as_view(), name='debit-energie-detail'),
    path('api/local/<int:pk>/', views.LocalDetailView.as_view(), name='local-detail'),
    path('api/produit/<int:pk>/', views.ProduitDetailView.as_view(), name='produit-detail'),
    path('api/utilisation-matiere-premiere/<int:pk>/', views.UtilisationMatierePremiereDetailView.as_view(), name='utilisation-matiere-premiere-detail'),
    path('api/approvisionnement-matiere-premiere/<int:pk>/', views.ApprovisionnementMatierePremiereDetailView.as_view(), name='approvisionnement-matiere-premiere-detail'),
    path('api/ressource-humaine/<int:pk>/', views.RessourceHumaineDetailView.as_view(), name='ressource-humaine-detail'),
    path('api/machine/<int:pk>/', views.MachineDetailView.as_view(), name='machine-detail'),
    path('api/fabrication/<int:pk>/', views.FabricationDetailView.as_view(), name='fabrication-detail'),
]