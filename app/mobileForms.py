from .models import *
from django import forms
from django.forms import ModelForm



class commandeEditForm(ModelForm):

    class Meta:

        model = Commande
        fields = ['client' ,'telephone', 'adresse', 'total', 'remarque', 'statut', 'methode_livraison', 'mode',]

class infoNomForm(ModelForm):

    class Meta:

        model = Utilisateur
        fields = ['nom',]

class infoTelephoneForm(ModelForm):

    class Meta:

        model = Utilisateur
        fields = ['telephone',]

class infoEmailForm(ModelForm):

    class Meta:

        model = Utilisateur
        fields = ['email',]

