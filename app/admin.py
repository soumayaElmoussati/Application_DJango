from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
admin.site.register(Bulkclients)
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Mouvement)
admin.site.register(Commande)
admin.site.register(Order)
admin.site.register(Wilaya)
admin.site.register(Commune)
admin.site.register(Boutiques)
admin.site.register(Utilisateur)