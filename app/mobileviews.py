import imp
from django.db.models.aggregates import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as dj_login, authenticate, logout, get_user_model
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.utils import timezone
from .mobileForms import *
from django.contrib import messages




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

def mobilelogin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.statut == 'ACTIVE':
                dj_login(request, user)
                return redirect('/mainmobile')
            else:
                return handler500(request)
            
        else:
            print(user)
            return redirect('/')
    
    return render(request, 'mobile/auth.html', {})

@login_required
def mainmobile(request):
    user = get_object_or_404(User, username=request.user)
    
    data = Commande.objects.filter(livreur_agent=user)
    total_commande = data.count()

    total_commande_en_livraison = Commande.objects.filter(livreur_agent=user, mode='en_livraison').count()
    total_commande_livree = Commande.objects.filter(livreur_agent=user, mode='livree').count()
    total_commande_en_retour = Commande.objects.filter(livreur_agent=user, mode='en_retour').count()
    total_commande_annuler = Commande.objects.filter(livreur_agent=user, mode='annuler').count()
    

    context = {
        'nbar': 'dashboard',
        'totalcommande': total_commande,
        'data': data,
        'd': total_commande_en_livraison,
        'e': total_commande_livree,
        'f': total_commande_en_retour,
        'g': total_commande_annuler
    }

    return render(request, 'mobile/main.html', context)

@login_required
def commandetotal(request):
    user = get_object_or_404(User, username=request.user)
    
    data = Commande.objects.filter(livreur_agent=user).order_by('-id')


    
    context = {
        'nbar': 'commande',
        'data': data
    }

    return render(request, 'mobile/commande.html', context)

@login_required
def commandeEdit(request, pk):
    user = get_object_or_404(User, username=request.user)
    
    instance = get_object_or_404(Commande, pk=pk)
    
    if request.method == 'POST':
        editcommande = commandeEditForm(request.POST or None, instance=instance)

        if editcommande.is_valid():
            obj = editcommande.save(commit=False)
            obj.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
           
    else:
        editcommande = commandeEditForm(request.POST or None, instance=instance)
    
    context = {

        'form': editcommande,
        'tracking': instance.trackingnumber
    }

    return render(request, 'mobile/editcommande.html', context)

@login_required
def commandefiltred(request, type):
    user = get_object_or_404(User, username=request.user)
    
    data = Commande.objects.filter(livreur_agent=user, mode=str(type)).order_by('-id')
    context = {
        'commandestype': str(type).replace("_", " "),
        'data': data
    }

    return render(request, 'mobile/commandefiltred.html', context)

@login_required
def scannercommande(request):


    context = {
        'nbar': 'scanner'
    }

    return render(request, 'mobile/scanner.html', context)

@login_required
def settingsmobile(request):

    context = {
        'nbar': 'profil'
    }
    return render(request, 'mobile/settingsmobile.html', context)

@login_required
def formsEditor(request, forms):

    instance = get_object_or_404(User, username=request.user)

    editForms = eval(forms)
    
    if request.method == 'POST':
        edit = editForms(request.POST or None, instance=instance)

        if edit.is_valid():
            obj = edit.save(commit=False)
            obj.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
           
    else:
        edit = editForms(request.POST or None, instance=instance)

    context = {
        'form': edit
    }

    return render(request, 'mobile/infoEdit.html', context)

def logoutmobile(request):

    logout(request)
    return redirect('/mobilelogin')