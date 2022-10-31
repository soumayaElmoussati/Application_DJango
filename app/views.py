from django.db.models.aggregates import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as dj_login, authenticate, logout, get_user_model
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from .forms import *
from django.contrib import messages
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import qr
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
import textwrap, xlsxwriter, os, openpyxl, json
import pygsheets




BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

today = timezone.now().day
month = timezone.now().month
year = timezone.now().year

@login_required
def draw_wrapped_line(canvas, text, length, x_pos, y_pos, y_offset):
    """
    :param canvas: reportlab canvas
    :param text: the raw text to wrap
    :param length: the max number of characters per line
    :param x_pos: starting x position
    :param y_pos: starting y position
    :param y_offset: the amount of space to leave between wrapped lines
    """
    if len(text) > length:
        wraps = textwrap.wrap(text, length)
        for x in range(len(wraps)):
            canvas.drawString(x_pos, y_pos, wraps[x])
            y_pos -= y_offset
        y_pos += y_offset  # add back offset after last wrapped line
    else:
        canvas.drawString(x_pos, y_pos, text)
    return 


# en_Confir = Commande.objects.filter(mode="en_confirmation").count()
# en_prepa = Commande.objects.filter(mode="en_preparation").count()
# en_dispatch = Commande.objects.filter(mode="en_dispatch").count()
# en_livraison = Commande.objects.filter(mode="en_livraison").count()
# en_livr = Commande.objects.filter(mode="livree").count()
# en_retour = Commande.objects.filter(mode="en_retour").count()



def handler404(request, *args, **argv):


    return render(request, 'errorpages/500.html', {})

def handler500(request, *args, **argv):

    title='COMPTE NON ACTIVE !'
    
    context = {
        'errortitle': title
    }
    return render(request, 'errorpages/500.html', context)

def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.statut == 'ACTIVE':
                dj_login(request, user)
                return redirect('/dashboard/ans')
            else:
                return handler500(request)
            
        else:
            print(user)
            return redirect('/')
    
    return render(request, 'auth.html', {'nbar': 'LOGIN'})

@login_required
def panel(request, timePlage):

    sevenDayAgo = timezone.now() - timezone.timedelta(days=6)
    sevener = sevenDayAgo.day

    commandeCree = []
    commandeLivrer = []
    commandeRetour = []
    dataAnomalie = []
    commandeEncaisser = []
    commandeConfirmer = []
    sug = ["en_confirmation", "en_preparation", "en_dispatch", "en_livraison", "livree", "en_retour"]

    # STATISTIQUE ANNUEL
    if timePlage == "ans":
        # CHART PERFORMANCE

        total_commande = Commande.objects.filter(date__year=year).count()
    
        for y in sug:
            objt = Commande.objects.filter(date__year=year, mode=str(y)).count()
            obgrad = objt * 100 / total_commande
            obgrad = round(obgrad, 2)
            dataAnomalie.append(obgrad)

        for t in range(1, 13):
            dataYear = Commande.objects.filter(date__year=year, date__month=t).count()
            dataLivrer = Commande.objects.filter(date__year=year, date__month=t, mode="livree").count()
            dataRetour = Commande.objects.filter(date__year=year, date__month=t, mode="en_retour").count()
            commandeCree.append(dataYear)
            commandeLivrer.append(dataLivrer)
            commandeRetour.append(dataRetour)

        for t in range(1, 13):

            commandeEnc = Encaissement.objects.filter(date__year= year, date__month=t).count()
            commandeConfi = Commande.objects.filter(date__year= year, date__month=t, statut="CONFIRMER").count()
            commandeEncaisser.append(commandeEnc)
            commandeConfirmer.append(commandeConfi)

    # STATISTIQUE MENSUEL
    if timePlage == "mois":
        # CHART PERFORMANCE

        total_commande = Commande.objects.filter(date__year=year, date__month=month).count()
    
        for y in sug:
            objt = Commande.objects.filter(date__year=year, date__month=month, mode=str(y)).count()
            obgrad = objt * 100 / total_commande
            obgrad = round(obgrad, 2)
            dataAnomalie.append(obgrad)

        for t in range(1, 32):
            dataYear = Commande.objects.filter(date__year=year, date__month=month, date__day=t).count()
            dataLivrer = Commande.objects.filter(date__year=year, date__month=month, date__day=t, mode="livree").count()
            dataRetour = Commande.objects.filter(date__year=year, date__month=month, date__day=t, mode="en_retour").count()
            commandeCree.append(dataYear)
            commandeLivrer.append(dataLivrer)
            commandeRetour.append(dataRetour)

        for t in range(1, 32):

            commandeEnc = Encaissement.objects.filter(date__year= year,date__month=month, date__day=t).count()
            commandeConfi = Commande.objects.filter(date__year= year, date__month=month, date__day=t, statut="CONFIRMER").count()
            commandeEncaisser.append(commandeEnc)
            commandeConfirmer.append(commandeConfi)

    # STATISTIQUE HEBDOMADAIRE
    if timePlage == "semaine":
        # CHART PERFORMANCE

        total_commande = Commande.objects.filter(date__year=year, date__month=month).count()
    
        for y in sug:
            objt = Commande.objects.filter(date__year=year, date__month=month, mode=str(y)).count()
            obgrad = objt * 100 / total_commande
            obgrad = round(obgrad, 2)
            dataAnomalie.append(obgrad)
        
        lps = sevener
        for t in range(1, 8):
            dataYear = Commande.objects.filter(date__year=year, date__month=month, date__day=lps).count()
            dataLivrer = Commande.objects.filter(date__year=year, date__month=month, date__day=lps, mode="livree").count()
            dataRetour = Commande.objects.filter(date__year=year, date__month=month, date__day=lps, mode="en_retour").count()
            commandeCree.append(dataYear)
            commandeLivrer.append(dataLivrer)
            commandeRetour.append(dataRetour)
            lps = lps + 1

        sps = sevener
        for t in range(1, 8):

            commandeEnc = Encaissement.objects.filter(date__year= year,date__month=month, date__day=sps).count()
            commandeConfi = Commande.objects.filter(date__year= year, date__month=month, date__day=sps, statut="CONFIRMER").count()
            commandeEncaisser.append(commandeEnc)
            commandeConfirmer.append(commandeConfi)
            sps = sps + 1



    context = {
        'nbar': 'DASHBOARD',
        'analytics': timePlage,
        'totalCommande': total_commande,
        'c_Cree': commandeCree,
        'c_Livrer': commandeLivrer,
        'c_Retour': commandeRetour,
        'anomalie': dataAnomalie,
        'c_encaisser': commandeEncaisser,
        'c_confirm': commandeConfirmer,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'mainPage.html', context)

@login_required
def clientView(request):
    clients = Client.objects.all()


    context = {
        'clients' : clients,
        'nbar': 'CLIENTS',
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'clientsaffichage.html', context)

@login_required
def addclientView(request):

    if request.method == 'POST':
        user = Utilisateur.objects.get(username=request.user.username)
        addclient = clientsFrom(request.POST or None)
        print(addclient.errors)
        if addclient.is_valid():
            obj = addclient.save(commit=False)
            obj.date_inscription = timezone.now()
            obj.utilisateur = user
            obj.save()
            addclient = clientsFrom()
           
    else:
        
        addclient = clientsFrom()

    context = {
        'nbar': 'CLIENTS',
        'form': addclient,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'addclient.html', context)

@login_required
def importClients(request):

    if request.method == 'POST':
        agent = request.user
        file=request.FILES.get('bulkfile')
        print(file)
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        wb = openpyxl.load_workbook(file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["CLIENTS IMPORTATION BULK"]

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)

        # MODEL LIST GENEREATED ON excel_data
        #[
        # ['CLIENT', 'TELEPHONE', 'WILAYA', 'COMMUNE', 'ADRESSE', 'COMMANDES LIVREE (nombres)', 'COMMANDES RETOURNER (nombres)', 'COMMANDES ANNULEE (nombres)'], 
        # ['CLIENT 1', '8888', 'STIFA', 'STIFA', 'AVN 232', '0', '0', '0'], 
        # ['CLIENT 2 ', '873487', 'OUARAN', 'OUARAN', 'AVN 434', '4', '0', '2']
        # ]
        counter = 0
        for i in excel_data:
            if counter < 1:
                pass
            else:
                Client.objects.create(nom_complet=i[0], telephone=i[1], adresse=i[4], wilaya=i[2], commune=i[3])
            counter += 1
        messages.success(request, 'LISTE CLIENTS EST IMPORTER ACVEC SUCCES')
        return render(request, 'importclts.html', {'uploaded_file_url': uploaded_file_url})

        # Bulkclients.objects.create(
        #     agent = agent,
        #     file = uploaded_file_url,
        # ).save()




    context = {
        'nbar': 'IMPORT CLIENTS',
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'importclts.html', context)




@login_required
def downloadfile(request):
    output = BytesIO()

    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(name="CLIENTS IMPORTATION BULK")
    style = workbook.add_format({'bold': 4, 'border': 5, 'align': 'center', 'valign': 'vcenter','fg_color': 'E09F5A', 'font_size': '20'})
    styleHeader = workbook.add_format({'bold': 2, 'border': 5, 'align': 'center', 'valign': 'center'})
    worksheet.set_column(0, 7, 25)
    worksheet.write(0, 0, "CLIENT", styleHeader)
    worksheet.write(0, 1, "TELEPHONE", styleHeader)
    worksheet.write(0, 2, "WILAYA", styleHeader)
    worksheet.write(0, 3, "COMMUNE", styleHeader)
    worksheet.write(0, 4, "ADRESSE", styleHeader)
    worksheet.write(0, 5, "COMMANDES LIVREE (nombres)", styleHeader)
    worksheet.write(0, 6, "COMMANDES RETOURNER (nombres)", styleHeader)
    worksheet.write(0, 7, "COMMANDES ANNULEE (nombres)", styleHeader)



    workbook.close()
    output.seek(0)
    filename = 'MODEL-IMPORATION-BULK.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

################################################
################# Products #####################
################################################


@login_required
def ajouteproduit(request):
    
    
    if request.method == 'POST':    
        addarticle = productForm(request.POST, request.FILES)
        print(addarticle.errors)
        if addarticle.is_valid():
            addarticle.save()
            redirect('/addprod')
           
    else:
        addarticle = productForm()
        
    context = {
        'nbar': 'AJOUTER PRODUITS',
        'form': addarticle,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'addproduct.html', context)

@login_required
def prodeditor(request, pk):

    object = get_object_or_404(Product, pk=pk)
    addarticle = productForm(request.POST, request.FILES, instance=object)
    if request.method == 'POST':
        if addarticle.is_valid():
            addarticle.save()
            redirect('/addprod')
           
    else:
        redirect('/addprod')

    context = {
        'nbar': 'AJOUTER PRODUITS',
        'form': addarticle,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'addproduct.html', context)

@login_required
def importprodlist(request):

    context = {
        'nbar': 'IMPORT PRODUITS',
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'importbulkprod.html', context)

@login_required
def produits(request):

    data = Product.objects.all()

    context = {
        'nbar': 'LISTS PRODUITS',
        'data': data,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'produits.html', context)

@login_required
def variationprod(request):

    data = Variation.objects.all()

    if request.method == 'POST':
        addvariation = variationForm(request.POST or None)

        if addvariation.is_valid():
            addvariation.save()
            addvariation = variationForm()
           
    else:
        addvariation = variationForm()

    context = {
        'nbar': 'VARIATIONS',
        'form': addvariation,
        'variation': data,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'variations.html', context)

@login_required
def downloadfileproduct(request):

    filename = 'productsmodel.xlsx'
    file_path = BASE_DIR + '/modelfile/' + filename
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@login_required
def statisprod(request):
    
    produit = Product.objects.all()
    entity = []
    data = []
    dict = {}
    for t in produit:
        produit = get_object_or_404(Product, pk=t.pk)
        tComm = Commande.objects.filter().filter(order__produit=produit).count()
        tAnnul = Commande.objects.filter(mode="annuler").filter(order__produit=produit).count()
        tConfirm = Commande.objects.filter(mode="en_confirmation").filter(order__produit=produit).count()
        tPrepa = Commande.objects.filter(mode="en_preparation").filter(order__produit=produit).count()
        tDisp = Commande.objects.filter(mode="en_dispatch").filter(order__produit=produit).count()
        tLivrais = Commande.objects.filter(mode="en_livraison").filter(order__produit=produit).count()
        tLivrer = Commande.objects.filter(mode="livree").filter(order__produit=produit).count()
        tRetour = Commande.objects.filter(mode="en_retour").filter(order__produit=produit).count()
        data.append(produit.nom_francais)
        data.append(produit.reference)
        data.append(tComm)
        data.append(tAnnul)
        data.append(tConfirm)
        data.append(tPrepa)
        data.append(tDisp)
        data.append(tLivrais)
        data.append(tLivrer)
        data.append(tRetour)
        entity.append(data)
        data = []
    
    dict['data'] = entity


    return JsonResponse(dict, safe=False)


################################################
################# STOCKS #######################
################################################

@login_required
def importstock(request):

    if request.method == 'POST':
        agent = request.user
        file=request.FILES.get('bulkfile')
        print(file)
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        wb = openpyxl.load_workbook(file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Produits"]

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)



        for i in excel_data[1:]:
            produit = Product.objects.filter(reference=i[0]).first()
            Mouvement.objects.create(produit=produit, motif=i[1], qte=i[4], date=timezone.now(), agent=request.user)
      
        
        return render(request, 'importstock.html', {'uploaded_file_url': uploaded_file_url})



    context = {
        'nbar': 'IMPORTATION STOCK',
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'importstock.html', context)

@login_required
def downloadfilestock(request):

    filename = 'stocksmodel.xlsx'
    file_path = BASE_DIR + '/modelfile/' + filename
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@login_required
def inventairedata(request):
    
    produit = Product.objects.all()
    entity = []
    data = []
    dict = {}
    for t in produit:
        qte = Mouvement.objects.filter(produit=t.pk).aggregate(Sum("qte")).get("qte__sum")
        if qte == None:
            qte = 0
        data.append(t.pk)
        data.append("<img src="+t.image_1.url+" style=\"width: 40px; heigth: auto;\">")
        data.append(t.reference)
        data.append(t.nom_francais)
        data.append("en vente")
        data.append("en commande")
        data.append("confirmer")
        data.append("Dispatch")
        if qte > 0:
            data.append("<span class=\"badge rounded-pill bg-success float-end\" key=\"t-new\">"+str(qte)+"</span>")
        else:
            data.append("<span class=\"badge rounded-pill bg-danger float-end\" key=\"t-new\">"+str(qte)+"</span>")
        data.append("Manquante")
        data.append("en livraison")
        data.append("en retour")
        btq = []
        for u in t.boutique.all():
            btq.append(u.nom)
        data.append(btq)
        data.append(t.is_Active)
        data.append("action")
        entity.append(data)
        data = []
    
    dict['data'] = entity


    return JsonResponse(dict, safe=False)

@login_required
def inventaire(request):

    data = Product.objects.all()

    context = {
        'nbar': 'INVENTAIRE',
        'data': data,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'inventaire.html', context)

@login_required
def mouvement(request):


    data = Mouvement.objects.all()

    if request.method == 'POST':
        addvariation = mouvementFrom(request.POST or None)

        if addvariation.is_valid():
            obj = addvariation.save(commit=False)
            obj.date = timezone.now()
            obj.agent = request.user
            obj.save()
            addvariation = mouvementFrom()
           
    else:
        addvariation = mouvementFrom()

    context = {
        'nbar': 'MOUVEMENTS',
        'data': data,
        'form': addvariation,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'mouvement.html', context)



################################################
################# FRS & MARQUE #################
################################################

@login_required
def fournisseur(request):

    data = Fournisseur.objects.all()

    if request.method == 'POST':
        addvariation = frsForm(request.POST or None)

        if addvariation.is_valid():
            obj = addvariation.save(commit=False)
            obj.date = timezone.now()
            obj.agent = request.user
            obj.save()
            addvariation = frsForm()
           
    else:
        addvariation = frsForm()

    context = {
        'nbar': 'FOURNISSEUR',
        'data': data,
        'form': addvariation,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'fournisseur.html', context)

@login_required
def marque(request):

    data = Marque.objects.all()

    if request.method == 'POST':
        addvariation = marqueForm(request.POST or None)

        if addvariation.is_valid():
            obj = addvariation.save(commit=False)
            obj.save()
            addvariation = marqueForm()
           
    else:
        addvariation = marqueForm()

    context = {
        'nbar': 'MARQUE',
        'data': data,
        'form': addvariation,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'marque.html', context)


################################################
################# LIVRAISON ####################
################################################

@login_required
def livraison(request):

    data = Livraison.objects.all()

    if request.method == 'POST':
        addvariation = livraisonForm(request.POST or None)

        if addvariation.is_valid():
            obj = addvariation.save(commit=False)
            obj.save()
            addvariation = livraisonForm()
           
    else:
        addvariation = livraisonForm()

    context = {
        'nbar': 'LIVRAISON',
        'data': data,
        'form': addvariation,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'livraison.html', context)

@login_required
def livraisonfrais(request):

    context = {
        'nbar': 'FRAIS LIVRAISON',
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'livraisonfrais.html', context)

################################################
################## BOUTIQUES ###################
################################################

@login_required
def boutiques(request):

    data = Boutiques.objects.all()

    if request.method == 'POST':
        addboutique = boutiqueForm(request.POST or None)

        if addboutique.is_valid():
            obj = addboutique.save(commit=False)
            obj.save()
            addboutique = boutiqueForm()
           
    else:
        addboutique = boutiqueForm()


    context = {
        'nbar': 'BOUTIQUES',
        'data': data,
        'form': addboutique,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'boutiques.html', context)


################################################
################## Charge ######################
################################################

@login_required
def encaissement(request):

    data = Encaissement.objects.all()

    if request.method == 'POST':
        addencaissement = encaissementForm(request.POST or None)

        if addencaissement.is_valid():
            obj = addencaissement.save(commit=False)
            obj.date = timezone.now()
            obj.agent = request.user
            obj.save()
            addencaissement = encaissementForm()
            return redirect('/encaissement')
           
    else:
        addencaissement = encaissementForm()

    context = {
        'nbar': 'ENCAISSEMENTS',
        'data': data,
        'form': addencaissement,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'encaissement.html', context)


@login_required
def charge(request):

    data = Charge.objects.all()

    if request.method == 'POST':
        addcharge = chargeForm(request.POST or None)

        if addcharge.is_valid():
            obj = addcharge.save(commit=False)
            obj.date_saisie = timezone.now()
            obj.agent = request.user
            obj.save()
            addcharge = chargeForm()
           
    else:
        addcharge = chargeForm()

    context = {
        'nbar': 'CHARGE',
        'data': data,
        'form': addcharge,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'charge.html', context)


################################################
############ Module Moderateurs ################
################################################

@login_required
def moderateurs(request):

    User = get_user_model()
    users = User.objects.all()
    if request.method == 'POST':
        form = moderateurForm(request.POST)
        if form.is_valid():
            user = form.save()
            # group = Group.objects.get(name='serveur')
            # user.groups.add(group)
            return redirect('/moderateurs')
    else:
        form = moderateurForm()

    context = {
        'form': form,
        'data': users,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }
    return render(request, 'moderateurs.html', context)


################################################
########## GENERAL CONFIGURATION ###############
################################################




@login_required
def role(request):
    data = Group.objects.all()
    form = UserGroupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()

        else:
            form = UserGroupForm(request.POST or None)

    context = {
        'nbar': 'AJOUTE ROLE',
        'form': form,
        'data': data,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'addrole.html', context)

@login_required
def configuration(request):


    context = {
        'nbar': 'PARAMERTRAGE',
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'settings.html', context)



@login_required
def googleSheet(request, worksheet, user):

    # arrays returned 
    user = get_object_or_404(User, pk=user)
    #[
    # '2022-02-03 ', DATE
    # '1', ID
    # 'PROD 1',  PRODUIT
    # 'TEST ME', CLIENT
    # '09 909 09 09', NUMERO
    # ' ORAN', WILAYA
    # '', SKU
    # '2', QTE
    # '32', ADRESSE
    # '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    productUnfound = []
    gc = pygsheets.authorize(service_file='{}'.format(user.googleSheetApi.url))
    sh = gc.open(str(worksheet))
    wks = sh.sheet1
    wks = list(wks)
    for row in wks[1:]:
        client = Client.objects.get_or_create(nom_complet=str(row[3]))
        try:
            client = get_object_or_404(Client, nom_complet=str(row[3]))

            wilys = Wilaya.objects.filter(nom__icontains= str(row[5])).first()

            if wilys == None:

                wilys = Wilaya.objects.create(nom=str(row[5]))

            wilaya = get_object_or_404(Wilaya, pk=wilys.pk)
            print(str(row[2]))
            produit = Product.objects.filter(nom_francais=str(row[2])).first()
            
            boutique = get_object_or_404(Boutiques, pk=1)
            commande = Commande.objects.create(
                date=timezone.now(),
                boutique=boutique,
                agent=str(request.user),
                client=client,
                telephone=str(row[4]),
                wilaya=wilaya,
                adresse=str(row[8]),
                mode="en_confirmation",
                )

            # add Orders
            commandeInstance = get_object_or_404(Commande, pk=commande.pk)

            if produit == None:
                continue
            else:
                produitInstance = get_object_or_404(Product, pk=produit.pk)
                prix=float(produit.prix_vente)

                Order.objects.create(
                    commande=commandeInstance,
                    produit=produitInstance,
                    prix=prix,
                    qte = int(row[7]),
                    total_order = float(prix)*int(row[7]),
                )
                print("CREATED COMMANDE")
            
        except Product.DoesNotExist:
            productUnfound.append(str(row[2]))
            continue

    print(productUnfound)

    return redirect('/dashboard/ans')

@login_required
def deleteview(request, link, pk):

    if link == 'User':
        modelName = eval(link)
        obj = get_object_or_404(modelName, pk=pk)
        obj.is_active == False
        obj.delete()
    else:
        modelName = eval(link)
        obj = get_object_or_404(modelName, pk=pk)
        obj.delete()


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def editview(request, modal, form, pk):

    modelName = eval(modal)
    formName = eval(form)
    instance = get_object_or_404(modelName, pk=pk)

    if request.method == 'POST':
        addvariation = formName(request.POST or None,  request.FILES or None, instance=instance)

        if addvariation.is_valid():
            obj = addvariation.save(commit=False)
            obj.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
           
    else:
        addvariation = formName(request.POST or None,  request.FILES or None, instance=instance)

    context = {
        'nbar': '{}'.format(modal),
        'form': addvariation,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'edit.html', context)


################################################
############## GENERAL COMMANDE ################
################################################

@login_required
def commande(request):

    array = []
    object = {}
    data = Product.objects.all()
    for i in data:
        object['id'] = i.pk
        object['text'] = i.nom_francais
        array.append(object)
        object = {}

    if request.method == 'POST':
        addcommande = commandeForm(request.POST)
        print(addcommande.errors)
        if addcommande.is_valid():
            obj = addcommande.save(commit=False)
            jsp = addcommande.cleaned_data['json_products']
            obj.agent = request.user
            obj.date = timezone.now()
            obj.save()
            idCommande = obj.id
            jsonProducts = json.loads(jsp)
            print(jsonProducts)
            for t in jsonProducts:
                produitInstance = get_object_or_404(Product, pk=int(t['produits']))
                commandeInstance = get_object_or_404(Commande, pk=idCommande)
                Order.objects.create(commande=commandeInstance, produit=produitInstance, prix=float(t['prix']), qte=int(t['qte']), total_order=float(t['prix'])*int(t['qte']))
            addcommande = commandeForm()
           
    else:
        
        addcommande = commandeForm()

    

    context = {
        'nbar': 'AJOUTE COMMANDE',
        'formCommande': addcommande,
        'dataproduits': array,
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }
    return render(request, 'commande.html', context)


def commandefilter(request, mode):

    data = Commande.objects.filter(mode=mode).order_by('-id')

    context = {
        'nbar': 'COMMANDE ' + str(mode),
        'data': data,
        'mode': str(mode).upper().replace('_', ' '),
        'a': en_Confir,
        'b': en_prepa,
        'c': en_dispatch,
        'd': en_livraison,
        'e': en_livr,
        'f': en_retour
    }

    return render(request, 'commandeliste.html', context)

def commandePdf(request, pk):
    infoCommande = get_object_or_404(Commande, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Commande|#{}.pdf"'.format(str(pk).zfill(6))

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    #page size 14.81cm x 21.01 cm

    p.setPageSize((794.07874016, 559.7480315))
    p.setFont('Helvetica', 35)
    p.setFillColor('#3f4041')
    logo = ImageReader('http://'+str(request.get_host())+'/static/label/label.png')
    #page size 14.81cm x 21.01 cm
    p.drawImage(logo, 0, 0, 794.07874016, 559.7480315, mask='auto')

    # draw a QR code
    qr_code = qr.QrCodeWidget('{}'.format(infoCommande.trackingnumber))
    bounds = qr_code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    d = Drawing(45, 45, transform=[45./width,0,0,45./height,0,0])
    d.add(qr_code)
    renderPDF.draw(d, p, 640, 490)


    p.setFillColor('#000000')
    p.setFont('Helvetica-Bold', 25)
    p.drawCentredString(558, 420, "#{}".format(str(infoCommande.pk).zfill(6)))

    p.setFillColor('#000000')
    p.setFont('Helvetica', 11)
    # RIGHT INFO SIDE
    p.drawString(100, 434, "{}".format(infoCommande.client))
    p.drawString(110, 422, "{}".format(infoCommande.telephone))
    p.drawString(98, 407, "{}".format(infoCommande.adresse))
    p.drawString(110, 394, "{}".format(infoCommande.commun))
    p.drawString(110, 382, "{}".format(infoCommande.remarque))
    p.drawString(110, 368, "{}".format(infoCommande.date.strftime("%d-%m-%Y | %H:%M") ))
    # LEFT INFO SIDE
    p.drawString(560, 401, "{}".format(infoCommande.wilaya))
    p.drawString(560, 388, "{}".format(infoCommande.livreur_agent))
    p.drawString(560, 374, "{}".format(infoCommande.methode_livraison))


    # PRODUCT INFO
    orders = Order.objects.filter(commande=infoCommande).first()
    p.drawCentredString(87, 319, "{}".format(orders.produit.reference))
    p.drawCentredString(230, 319, "{}".format(orders.produit.nom_francais))
    p.drawCentredString(357, 319, "{}".format(orders.qte))
    p.drawCentredString(510, 319, "{}".format(orders.prix))
    p.drawCentredString(687, 319, "{}".format(orders.total_order))


    # TOTAL INFO

    p.drawCentredString(687, 299, "{}".format(infoCommande.sous_total))

    p.drawCentredString(687, 279, "{}".format(infoCommande.reduction))

    p.drawCentredString(687, 259, "{}".format(infoCommande.livraison))

    p.drawCentredString(687, 239, "{}".format(infoCommande.total))
    

    # BOUTIQUE INFO
    p.drawString(70, 50, "{}".format(infoCommande.boutique.email))
    p.drawString(345, 50, "{}".format(infoCommande.boutique.siteweb))
    p.drawString(650, 50, "{}".format(infoCommande.boutique.numero_service_client))


    # p.setFillColor('#0870a5')
    # p.setFont('Helvetica-Bold', 44)

    #p.drawCentredString(280, a, '{}'.format(r.article.refer))

    
    #draw_wrapped_line(p, fac.piedPage, 60, 180, 980, 80)

    

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response



#############################################################################################
#############################################################################################
###################################### CLIENT ESPACE ########################################
#############################################################################################
#############################################################################################

@login_required
def boutiquejson(request):
    
    user = get_object_or_404(User, username=request.user)
    bqt = Boutiques.objects.filter(utilisateur=user)

    data = []

    for t in bqt:
       dict = {}
       dict['id'] = t.pk
       dict['text'] = t.nom
       data.append(dict)

    return JsonResponse({"results": data})




def clientsProfil(request):

    user = User.objects.get(username=request.user.username)
    encaisser = Commande.objects.filter(utilisateur=user, encaisser='OUI').count()
    pending = Commande.objects.filter(utilisateur=user, mode='en_livraison').count()
    t_encaisse = Commande.objects.filter(utilisateur=user, encaisser='OUI').aggregate(Sum('total')).get('total__sum')

    context = {
        'nbar': 'PROFIL',
        'user': user, 
        'encaissement':encaisser,
        'pending': pending,
        't_encaissement': t_encaisse
    }

    return render(request, 'client_template/profil.html', context)


def logoutPage(request):

    logout(request)
    return redirect('/')