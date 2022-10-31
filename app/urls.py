from .views import *
from .mobileviews import *
from django.urls import path

app_name = 'app'


urlpatterns = [
    
    path('', login, name='login'),
    path('dashboard/<str:timePlage>', panel, name="dashboard"),
    path('statisprod', statisprod, name="statisprod"),
    #module Client
    path('clients', clientView, name="clients"),
    path('addclient', addclientView, name="addclient"),
    path('importclts', importClients, name="importclts"),
    path('modelfile', downloadfile, name='modelfile'),
    #MODULE PRODUITS
    path('addprod', ajouteproduit, name='addprod'),
    path('bulkprod', importprodlist, name='bulkprod'),
    path('prodeditor/<str:pk>', prodeditor, name='prodeditor'),
    path('produits', produits, name='produits'),
    path('variations', variationprod, name='variations'),
    path('downloadfileproduct',downloadfileproduct, name='downloadfileproduct'),
    # MODULE STOCK
    path('importstock', importstock, name='importstock'),
    path('downloadstockmodel', downloadfilestock, name='downloadstockmodel'),
    #data mega inventaire
    path('inventairedata', inventairedata, name='inventairedata'),
    path('inventaire', inventaire, name='inventaire'),
    path('mouvement', mouvement, name='mouvement'),
    

    # MODULE FRS & MARQUE

    path('fournisseur', fournisseur, name='fournisseur'),
    path('marque', marque, name='marque'),


    # MODULE LIVRAISON

    path('livraison', livraison, name='livraison'),
    path('livraisonfrais', livraisonfrais, name='livraisonfrais'),

    # MODULE BOUTIQUE

    path('boutiques', boutiques, name='boutiques'),

    # MODULE CHARGE

    path('charge', charge, name='charge'),
    path('encaissement', encaissement, name='encaissement'),

    # FONCTIONALITE COMMANDE
    path('commande', commande, name='commande'),
    path('commandefilter/<str:mode>', commandefilter, name='commandefilter'),
    path('commandePdf/<str:pk>', commandePdf, name='commandePdf'),

    path('moderateurs', moderateurs, name='moderateurs'),
    path('role', role, name='role'),

    # general url
    path('googleSheet/<str:worksheet>', googleSheet, name='googleSheet'),
    path('settings', configuration, name='settings'),
    path('deleter/<str:link>/<str:pk>', deleteview, name='deleter'),
    path('editor/<str:modal>/<str:form>/<str:pk>', editview, name='editor'),
    path('logout', logoutPage, name="logout"),

    # espace clients

    path('profil', clientsProfil, name='profil'),
    path('boutiquejson', boutiquejson, name='boutiquejson'),


    # MOBILE VIEWS


    path('mobilelogin', mobilelogin, name='mobilelogin'),
    path('mainmobile', mainmobile, name='mainmobile'),
    path('commandetotal', commandetotal, name='commandetotal'),
    path('commandeEdit/<str:pk>', commandeEdit, name='commandeEdit'),
    path('commandefiltred/<str:type>', commandefiltred, name='commandefiltred'),
    path('scannercommande', scannercommande, name='scannercommande'),

    path('settingsmobile', settingsmobile, name='settingsmobile'),
    path('formsEditor/<str:forms>', formsEditor, name='formsEditor'),
    path('logoutmobile', logoutmobile, name='logoutmobile'),
]