from io import BytesIO
from random import randint
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import AbstractUser, BaseUserManager
from PIL import Image
import sys, os

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='DELETED USER')[0]

# functions of upload path generator
def uploadito(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'profils/user_{0}/{1}'.format(instance.nom, filename)


#wilaya commun
class Wilaya(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom

class Commune(models.Model):
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom


# model clients
class Client(models.Model):
    
    date_inscription = models.DateTimeField()
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.SET(get_sentinel_user), null=True)
    nom_complet = models.CharField(max_length=200)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.CharField(max_length=600, blank=True, null=True)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True, blank=True)
    commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return str(self.nom_complet)

# model pour enregistrement des fichier import clients

class Bulkclients(models.Model):

    agent = models.CharField(max_length=90, blank=True, null=True)
    date = models.DateTimeField(auto_now=timezone.now())
    file = models.FilePathField()


#####################################################
#####################################################
################ MODULE PRODUITS ####################
#####################################################
#####################################################


class Product(models.Model):

    LOGICAL = (
        ('OUI', 'OUI'),
        ('NON', 'NON'),
    )


    LOGICAL2 = (
        ('OUI', 'OUI'),
        ('NON', 'NON'),
    )


    LOGICAL3 = (
        ('OUI', 'OUI'),
        ('NON', 'NON'),
    )

    STAT = (
        ('OUI', 'ACTIVE'),
        ('NON', 'INACTIVE'),
    )

    TARIFS = (
        ('OUI', 'OPTION 1'),
        ('NON', 'OPTION 2'),
    )

    boutique = models.ManyToManyField('Boutiques', null=True)
    nom_francais = models.CharField(max_length=900)
    nom_arabe = models.CharField(max_length=900, blank=True, null=True)
    reference = models.CharField(max_length=900, blank=True, null=True, unique=True)
    code_barre = models.CharField(max_length=1000, blank=True, null=True)
    marque = models.ForeignKey('Marque', on_delete=models.PROTECT, null=True)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.PROTECT, null=True)
    prix_vente = models.FloatField()
    prix_achat = models.FloatField(blank=True, null=True)
    reduction = models.FloatField(blank=True, null=True)
    prix_promo = models.FloatField(blank=True, null=True)
    produit_avec_option = models.CharField(max_length=90, choices=LOGICAL)
    prix_option = models.CharField(max_length=90, choices=LOGICAL2)
    alert_rupture = models.CharField(max_length=90, choices=LOGICAL3)
    minimum_stock_alert = models.FloatField(blank=True, null=True)
    is_Active = models.CharField(max_length=90, choices=STAT)
    image_1 = models.FileField(upload_to='product/', default='product/product.png')
    image_2 = models.FileField(upload_to='product/', blank=True, null=True)
    image_3 = models.FileField(upload_to='product/', blank=True, null=True)
    image_4 = models.FileField(upload_to='product/', blank=True, null=True)
    image_5 = models.FileField(upload_to='product/', blank=True, null=True)
    image_6 = models.FileField(upload_to='product/', blank=True, null=True)
    tarifs_livraison = models.CharField(max_length=90, choices=TARIFS)
    wilayas = models.ManyToManyField(Wilaya, null=True)
    json_tarifs = models.CharField(max_length=9000, blank=True, null=True)
    def __str__(self):
        
        return str(self.reference)

class Variation(models.Model):

    TYPE = (
        ('couleur', 'couleur'),
        ('taille', 'taille'),
        ('pointure', 'pointure'),
    )
    nom_francais = models.CharField(max_length=100)
    nom_arabe = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE)
    is_active = models.BooleanField()


#####################################################
#####################################################
################ MODULE STOCK ####################
#####################################################
#####################################################

class Mouvement(models.Model):

    date = models.DateTimeField()
    agent = models.CharField(max_length=90)
    produit = models.ForeignKey(Product, on_delete=models.PROTECT)
    motif = models.CharField(max_length=400, blank=True, null=True)
    qte = models.IntegerField()

#####################################################
#####################################################
################ MODULE FRS & MARQUE ################
#####################################################
#####################################################


class Fournisseur(models.Model):

    STAT = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )
    date = models.DateTimeField()
    agent = models.CharField(max_length=90)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=130, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STAT)
    def __str__(self):
        
        return str(self.nom)
class Marque(models.Model):
    
    
    STAT = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )

    POSI = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
    )
    nom = models.CharField(max_length=400)
    position = models.CharField(max_length=10, choices=POSI)
    boutique = models.ForeignKey('Boutiques', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=30, choices=STAT)
    def __str__(self):
        
        return str(self.nom)

#####################################################
#####################################################
################## MODULE LIVRAISON #################
#####################################################
#####################################################

class Livraison(models.Model):

    STAT = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )

    nom = models.CharField(max_length=400)
    telephone = models.CharField(max_length=40)
    boutique = models.ForeignKey('Boutiques', on_delete=models.DO_NOTHING)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True)
    platforme = models.CharField(max_length=400)
    status = models.CharField(max_length=30, choices=STAT)

    def __str__(self):
        
        return self.nom


#####################################################
#####################################################
################ MODULE Commande ####################
#####################################################
#####################################################


class Commande(models.Model):

    CHOICES = (
        ('LIVRAISON A DOMICILE', 'LIVRAISON A DOMICILE'), 
        ('STOP DESK', 'STOP DESK'),
    )
    STATUT = (
        ('CONFIRMER', 'CONFIRMER'),
        ('EN ATTENT', 'EN ATTENT'),

    )
    PROCESS = (
        ('en_confirmation', 'en_confirmation'),
        ('en_preparation', 'en_preparation'),
        ('en_dispatch', 'en_dispatch'),
        ('en_livraison', 'en_livraison'),
        ('livree', 'livree'),
        ('en_retour', 'en_retour'),
        ('annuler', 'annuler')
    )
    ENCAISSER = (
        ('OUI', 'OUI'),
        ('NON', 'NON'),
    )
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.SET(get_sentinel_user), null=True)
    date = models.DateTimeField(blank=True, null=True)
    agent = models.CharField(max_length=150, blank=True, null=True)
    boutique = models.ForeignKey('Boutiques', on_delete=models.DO_NOTHING, blank=True, null=True)
    methode_livraison = models.CharField(max_length=100, blank=True, null=True, choices=CHOICES)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    email = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    livreur_agent = models.ForeignKey('Utilisateur', on_delete=models.SET(get_sentinel_user), null=True, related_name='livreur')
    telephone_second = models.CharField(max_length=100, blank=True, null=True)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True, blank=True)
    commun = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)
    adresse = models.CharField(max_length=100, blank=True, null=True)
    remarque = models.CharField(max_length=100, blank=True, null=True)
    referent = models.CharField(max_length=100, blank=True, null=True)
    sous_total = models.FloatField(blank=True, null=True)
    livraison = models.FloatField(blank=True, null=True)
    reduction = models.FloatField(blank=True, null=True)
    echange = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    statut = models.CharField(max_length=100, blank=True, null=True, choices=STATUT)
    mode = models.CharField(max_length=100, null=True, blank=True, choices=PROCESS)
    encaisser = models.CharField(max_length=100, null=True, blank=True, choices=ENCAISSER)
    json_products = models.CharField(max_length=9000, blank=True, null=True)
    trackingnumber = models.CharField(max_length=9000, blank=True, null=True)

    def __str__(self):
        return "#"+str(self.pk).zfill(6)
    
    def save(self, *args, **kwargs):
        self.trackingnumber = str("C{}{}{}".format(randint(11, 99), randint(100, 999), randint(100, 980)))
        
        super(Commande, self).save(*args, **kwargs)

class Order(models.Model):
    POSI = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
    )

    commande = models.ForeignKey(Commande, on_delete=models.DO_NOTHING)
    produit = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    option = models.CharField(max_length=100, blank=True, null=True, choices=POSI)
    prix = models.FloatField(blank=True, null=True)
    qte = models.IntegerField(blank=True, null=True)
    total_order = models.FloatField(blank=True, null=True)


#####################################################
#####################################################
################ MODULE Boutiques ###################
#####################################################
#####################################################

class Boutiques(models.Model):

    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.SET(get_sentinel_user), null=True, blank=True)
    logo =  models.FileField(upload_to='boutique/', default='product/product.png')
    nom = models.CharField(max_length=150)
    adresses = models.CharField(max_length=120, blank=True, null=True)
    email = models.CharField(max_length=120, blank=True, null=True)
    siteweb = models.CharField(max_length=120, blank=True, null=True)
    numero_service_client = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        
        return self.nom


#####################################################
#####################################################
################### MODULE Charge ###################
#####################################################
#####################################################

class Charge(models.Model):

    TYPE = (
        ('CHARGE 1', 'CHARGE 1'),
        ('CHARGE 2', 'CHARGE 2'),
    )

    type_charge = models.CharField(max_length=200, blank=True, null=True, choices=TYPE)
    boutique =  models.ForeignKey(Boutiques, on_delete=models.RESTRICT)
    montant = models.FloatField()
    commentaire = models.CharField(max_length=200, blank=True, null=True)
    agent = models.CharField(max_length=200, blank=True, null=True)
    date_comptabiliser = models.DateField()
    date_saisie = models.DateTimeField()

#####################################################
#####################################################
############# MODULE Encaissement ###################
#####################################################
#####################################################

class Encaissement(models.Model):

    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    montant = models.FloatField(blank=True, null=True)
    agent = models.CharField(max_length=150, blank=True, null=True)


#####################################################
#####################################################
#################### MODULE Users ###################
#####################################################
#####################################################


class Utilisateur(AbstractUser):

    class role_utilisateur(models.TextChoices):

        ADMIN = 'ADMIN', 'ADMIN'
        STAFF = 'STAFF', 'STAFF'
        LIVREUR = 'LIVREUR', 'LIVREUR'
        UTILISATEUR = 'UTILISATEUR', 'UTILISATEUR'

    base_role_utilisateur = role_utilisateur.ADMIN
    

    STATUS = (
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
    )
    
    date_inscription = models.DateTimeField(auto_now=timezone.now())
    # user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name="staff_user")
    photo_profil = models.FileField(upload_to=uploadito, default='profils/user.png')
    nom = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    adresse = models.CharField(max_length=600, blank=True, null=True)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True, blank=True)
    commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=60, choices=role_utilisateur.choices, null=True)
    googleSheetApi = models.FileField(upload_to=uploadito, blank=True, null=True)
    statut = models.CharField(max_length=200, blank=True, choices=STATUS)
    
    def save(self, *args, **kwargs):

        if not self.pk:
            self.role = self.base_role_utilisateur


        # Opening the uploaded image
        im = Image.open(self.photo_profil)

        if im.mode == "JPEG":
            pass
        elif im.mode in ["RGBA", "P"]:
            im = im.convert("RGB")

        output = BytesIO()
        # Resize/modify the image - desired short edge of 200 pixels
        original_width, original_height = im.size

        if original_width > original_height:  # landscape image
            aspect_ratio = round(original_width / original_height, 2)
            desired_height = 200
            desired_width = round(desired_height * aspect_ratio)
            im = im.resize((desired_width, desired_height), Image.ANTIALIAS)

        elif original_height > original_width:  # portrait image
            aspect_ratio = round(original_height / original_width, 2)
            desired_width = 200
            desired_height = round(desired_width * aspect_ratio)
            im = im.resize((desired_width, desired_height), Image.ANTIALIAS)

        elif original_height == original_width:  # square image
            desired_width = 200
            desired_height = 200
            # Resize the image
            im = im.resize((desired_width, desired_height), Image.ANTIALIAS)

        # after modifications, save it to the output
        im.save(output, format='JPEG', subsampling=0, quality=95)
        output.seek(0)

        # change the imagefield value to be the newly modified image value
        self.photo_profil = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.photo_profil.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
        super().save(*args, **kwargs)


# BASE USER MANAGER FOR QUERES

# livreur to return only livreur object Livreur.livreur.all()

class LivreurManager(BaseUserManager):

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Utilisateur.role_utilisateur.LIVREUR)


class StaffManager(BaseUserManager):

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Utilisateur.role_utilisateur.STAFF)

class UsershippiliManager(BaseUserManager):

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Utilisateur.role_utilisateur.UTILISATEUR)




class Livreur(Utilisateur):

    base_role_utilisateur = Utilisateur.role_utilisateur.LIVREUR

    livreur = LivreurManager()

    class Meta: 

        proxy = True
    

class Staff(Utilisateur):

    base_role_utilisateur = Utilisateur.role_utilisateur.STAFF

    staff = StaffManager()

    class Meta: 

        proxy = True
    
    
class Usershippili(Utilisateur):

    base_role_utilisateur = Utilisateur.role_utilisateur.UTILISATEUR

    usershippili = UsershippiliManager()

    class Meta: 

        proxy = True

    