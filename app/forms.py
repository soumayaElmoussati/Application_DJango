from .models import *
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
 




class clientsFrom(ModelForm):

    class Meta:

        model = Client
        fields = '__all__'
        #exclude = ('utilisateur', 'date_inscription',)

class productForm(ModelForm):

    class Meta:

        model = Product
        fields = "__all__"
        # widgets = {
        #     'nom_francais': forms.TextInput(attrs={'class':'col-6 ml-2', 'type':'text'}),
        #     'nom_arabe': forms.TextInput(attrs={'class':'col-6 ml-2', 'type':'text'}),
        #     'reference': forms.TextInput(attrs={'class':'col-6 ml-2', 'type':'text'}),
        #     'code_barre': forms.TextInput(attrs={'class':'col-6 ml-2', 'type':'text'}),
        #     'prix_vente': forms.NumberInput(),
        #     'prix_achat': forms.NumberInput(),
        #     'reduction': forms.NumberInput(),
        #     'prix_promo': forms.NumberInput(),
            
        # }

class productForm2(ModelForm):

    class Meta:

        model = Product
        fields = "__all__"
        exclude = ('json_tarifs',)

class variationForm(ModelForm):

    class Meta:

        model = Variation
        fields = "__all__"

class mouvementFrom(ModelForm):

    class Meta:

        model = Mouvement
        fields = "__all__"
        exclude = ("date", "agent",)


class frsForm(ModelForm):

    class Meta:

        model = Fournisseur
        fields = '__all__'
        exclude = ("date", "agent",)


class marqueForm(ModelForm):

    class Meta:

        model = Marque
        fields = '__all__'


class livraisonForm(ModelForm):

    class Meta:

        model = Livraison
        fields = '__all__'


class commandeForm(ModelForm):

    class Meta:

        model = Commande
        fields = '__all__'
        exclude = ('trackingnumber',)

class commandeEditForm(ModelForm):

    class Meta:

        model = Commande
        fields = ['client', 'telephone', 'livreur_agent', 'remarque', 'statut', 'methode_livraison', 'mode']

class boutiqueForm(ModelForm):

    class Meta:

        model = Boutiques
        fields = '__all__'

class chargeForm(ModelForm):

    class Meta:

        model = Charge
        fields = '__all__'
        exclude = ('agent', 'date_saisie',)

class encaissementForm(ModelForm):

    class Meta:

        model = Encaissement
        fields = '__all__'
        exclude = ('agent', 'date',)

class SignupForm(ModelForm):

    class Meta:
        model = Utilisateur
        #fields = "__all__"
        fields = ('photo_profil', 'username', 'nom', 'telephone', 'email', 'statut', 'password', 'groups', 'role',)


class utilisateurForm(ModelForm):

    class Meta:
        model = Utilisateur
        #fields = "__all__"
        fields = ('photo_profil', 'nom', 'telephone', 'email', 'adresse', 'password', 'googleSheetApi',)
        widgets = {
            'password': forms.PasswordInput(),
        }