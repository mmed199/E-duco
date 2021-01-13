from django.shortcuts import *
from django.http import Http404
from cours.models import *
from .forms import *
from django.db.models import Count
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from random import randint
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login
from django.http import HttpResponseRedirect
from itertools import chain
# Create your views here.


#la vue du premiere page :
def index(request):
    form = rechercheForm(request.POST)
    if not request.user.is_authenticated :
        cr = Formations.objects.filter(ratings__isnull=False).order_by('-ratings__average')[:3]
        return render(request, 'index/index.html' , {'cours' : cr,'form' : form})
    else :
        formations = FormationsSuivis.objects.filter(utilisateur = request.user.utilisateurs)
        vos_formations = Formations.objects.filter(formation_utilisateur = request.user.utilisateurs)
       

        cr = Formations.objects.filter(ratings__isnull=False).order_by('-ratings__average')[:3]
        fini = formations.filter(fini = True).count()
        tous = formations.count()
        a = 0
        if tous != 0 :
            for formation in formations:
                order = Chapitres.objects.filter(course = formation.formation,order__lte = formation.chapitre.order).count()
                last = Chapitres.objects.filter(course = formation.formation).count()
                if last != 0:
                    a = a + ( order / last )
        
            a = (a / tous) * 100
        
        return render(request, 'index\dashboard.html', locals() )

@login_required()
def supprimer_chapitre(request, id , formation_id , commit ):
    if commit == 0:
        next = 'chapitre'
        message = 'Etes-vou sur de supprimer ce chapitre?'
        return render(request,'etes-vous-sur.html',locals())
    else:
        chapitre = get_object_or_404(Chapitres, id = id)
        if request.user.utilisateurs == chapitre.course.formation_utilisateur:
            chapitre.delete()
            return redirect('ajout_chapitre',formation_id)
        else :
            raise Http404

@login_required
def supprimer_formation(request, id , commit):
    if commit == 0:
        next = 'formation'
        message = 'Etes-vou sur de supprimer cette formation?'
        return render(request,'etes-vous-sur.html',locals())
    else:
        formation = get_object_or_404(Formations, id = id)
        if request.user.utilisateurs == formation.formation_utilisateur:
            formation.delete()
            return redirect('index')
        else :
            raise Http404   


def recherche(request):
    form = rechercheForm(request.POST)
    if form.is_valid():
        try:
            categorie = Categories.objects.get(categorie_nom__iexact = form.cleaned_data['input_recherche'])
            return redirect('cours/categories/{}'.format(categorie.id))
        except models.ObjectDoesNotExist as identifier:
            return redirect('cours/recherche/{}'.format(form.cleaned_data['input_recherche']))


#pre inscription , mote de passe et email
def pre_inscription(request):
    form = preInscriptionForm(request.POST)
    if form.is_valid(): 
        form_utis = inscriptionUtilisateur(request.POST)
        return render (request , 'inscription/compteUtis.html',{'email':form.cleaned_data['in_email'] ,
        'mdp' : form.cleaned_data['in_mdp'],'compte' : form.cleaned_data['in_compte'], 'form' : form_utis})
    else :
        return render (request , 'inscription/inscription.html',locals())



def utilisateur_inscription(request):
    form = inscriptionUtilisateur(request.POST)

    if form.is_valid():

        code = randint(1111,9999)
        user = User.objects.create_user(form.cleaned_data['in_email'],form.cleaned_data['in_email'],form.cleaned_data['in_mdp'],is_active = False)

        utis = Utilisateurs.objects.create(user=user, utilisateur_nom = form.cleaned_data['in_nom'].capitalize(),
        utilisateur_prenom = str(form.cleaned_data['in_prenom']).capitalize() , 
        utilisateur_date_naissance = form.cleaned_data['in_date_naissance'],
        utilisateur_genre = form.cleaned_data['in_genre'] , 
        utilisateur_statu = form.cleaned_data['in_statu'].capitalize(),
        utilisateur_code = code, 
        utilisateur_veut = form.cleaned_data['in_compte'])

        utis.save()

        mail_subject = 'Activate your Educo account.'

        message = render_to_string('acc_active_email.html', {
        'user': utis,
        'code':code
        })

        text_content = strip_tags(message)
        to_email = form.cleaned_data.get('in_email')

        email = EmailMultiAlternatives (
        mail_subject, message, to=[to_email]
        )

        email.attach_alternative(message , "text/html")
        #email.send()
        
        return redirect('verification/{}'.format(utis.id))
    
    return render(request,'inscription/compteUtis.html',{'form': form})


def verification(request,id_utilisateur):
    form = verificationForm(request.POST)
    utis = get_object_or_404(Utilisateurs, id = id_utilisateur)
    if form.is_valid():
        if (form.cleaned_data['in_code'] == utis.utilisateur_code):
                utis.user.is_active = True
                utis.user.save()
                return redirect('login')
    return render(request,'inscription/verification.html',locals())

    
    



def cours(request):
    form = rechercheForm(request.POST)
    cr = Formations.objects.raw('SELECT * FROM cours_Formations ORDER BY id DESC')
    ct = Formations.objects.values('formation_categorie__categorie_nom','formation_categorie').annotate(count=Count('formation_categorie'))

    return render(request,'cours/cours.html',locals())


def cours_categorie(request,id_categorie):
    form = rechercheForm(request.POST)

    cr = Formations.objects.filter(formation_categorie = id_categorie)
    ct = Formations.objects.values('formation_categorie__categorie_nom','formation_categorie').annotate(count=Count('formation_categorie'))

    return render(request,'cours/cours.html',locals())

def cours_recherche(request,recherche):
    form = rechercheForm(request.POST)
    cr = Formations.objects.filter(formation_libelle__icontains = recherche)
    ct = Formations.objects.values('formation_categorie__categorie_nom','formation_categorie').annotate(count=Count('formation_categorie'))
    return render(request,'cours/cours.html',locals())


def cours_display(request,id,slug):
    cours = get_object_or_404(Formations, id=id, formation_slug=slug)
    owner = False
    if request.user.is_authenticated:
        u = Utilisateurs.objects.filter(user = request.user)[0]
        
        if (u.id == cours.formation_utilisateur.id):
            owner = True
        
    premier_chapitre = Chapitres.objects.filter(course = cours).order_by('order')
    no_chapitre = True
    if premier_chapitre:
       no_chapitre = False 
       premier_chapitre = premier_chapitre[0].order

    
    form = rechercheForm(request.POST)
    if form.is_valid():
        try:
            categorie = Categories.objects.get(categorie_nom__iexact = form.cleaned_data['input_recherche'])
            return redirect('cours/categories/{}'.format(categorie.id))
        except models.ObjectDoesNotExist as identifier:
            return redirect('cours/recherche/{}'.format(form.cleaned_data['input_recherche']))


    plus = Formations.objects.filter(formation_categorie = cours.formation_categorie).exclude(id = id)[:3]
    count = plus.count()
    if (count == 0):
        plus = Formations.objects.filter(ratings__isnull=False).order_by('-ratings__average').exclude(id = id)[:3]    
    elif (count == 1):
        meilleur = Formations.objects.filter(ratings__isnull=False).exclude(id= plus[0].id).exclude(id = id).order_by('-ratings__average')[:2]
        plus = list(chain(plus , meilleur))
    elif (count == 2):
        meilleur = Formations.objects.filter(ratings__isnull=False).exclude(id = id).exclude(id = plus[0].id).exclude(id = plus[1].id).order_by('-ratings__average')[:1]
        plus = list(chain(plus , meilleur))

    return render(request, 'cours/cours_display.html', locals())



@login_required()
def chapitre_display(request,id,slug,order):
    chapitre = get_object_or_404(Chapitres, course = id , order = order)
    form = rechercheForm(request.POST)

    
    chapitres = Chapitres.objects.filter(course = id).order_by('order')
    
    chapitre_lu = FormationsSuivis.objects.filter(utilisateur = request.user.utilisateurs ,formation = id )
    if not chapitre_lu:
        FormationsSuivis.objects.create(utilisateur = request.user.utilisateurs,formation = get_object_or_404(Formations,id=id) , chapitre = chapitres[0])
        chapitre_lu = FormationsSuivis.objects.filter(utilisateur = request.user.utilisateurs ,formation = id )
    
    chapitre_lu = chapitre_lu[0]

    return render(request, 'cours/chapitre_display.html',locals())
    
@login_required()
def next_chapitre(request,id,order):
    
    formationUtilisateur = get_object_or_404(FormationsSuivis, id = id)
    if request.user.utilisateurs == formationUtilisateur.utilisateur:
        chapitres = Chapitres.objects.filter(course = formationUtilisateur.formation)
        
        if formationUtilisateur.chapitre.order == chapitres[chapitres.count()-1].order:
            formationUtilisateur.fini = True
            formationUtilisateur.save()
            return redirect('index')
        elif formationUtilisateur.chapitre.order == order :
            formationUtilisateur.chapitre = get_object_or_404(Chapitres , course = formationUtilisateur.formation , order = order + 1)
            formationUtilisateur.save()
            return redirect('chapitre_display', formationUtilisateur.formation.id , formationUtilisateur.formation.formation_slug , order + 1 )
        else :
            raise Http404
    else :
        raise Http404
        
        

    





def login(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                dj_login(request, user)  # nous connectons l'utilisateur
                #return redirect('../inscription')
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'connexion/login.html', locals())  

#
def comment_posted( request ):
    if request.GET['c']:
        post_id  = request.GET['c']
        post = Formations.objects.get( pk=post_id )

        if post:
            return redirect('../../{}/{}'.format(post.id,post.formation_slug))

    return HttpResponseRedirect( "/" )


#Ajout d'une formation
@login_required()
def ajout_formation(request):
    form = ajoutFormation(request.POST or None, request.FILES)
    if form.is_valid():
        u = Utilisateurs.objects.filter(user = request.user)[0]
        #return render(request,'formations/ajout_formation.html',locals())
        #if (c and u):
        f = Formations.objects.create(formation_libelle = form.cleaned_data['formation_libelle'] , formation_image = form.cleaned_data['formation_image'],
        formation_bio = form.cleaned_data['formation_bio'], formation_categorie = form.cleaned_data['formation_categorie'],
        formation_utilisateur = u)

        
    return render(request,'formations/ajout_formation.html',locals())


@login_required()
def ajout_chapitre(request,id):
    formation = get_object_or_404(Formations,id = id)
    u = Utilisateurs.objects.filter(user = request.user)[0]
    if (u.id == formation.formation_utilisateur.id):
        chapitres = Chapitres.objects.filter(course = formation)
        form = ajoutChapitres(request.POST or None, request.FILES)
        if form.is_valid():
            formation = Formations.objects.filter(id = id)[0]
            nv_chapitre = Chapitres.objects.create(course = formation , titre = form.cleaned_data['titre'] , 
            description = form.cleaned_data['description'] , contenu = form.cleaned_data['contenu'], image = form.cleaned_data['image'],
            fichier = form.cleaned_data['fichier'])
            redirect('/{}'.format(id))
            
        return render(request,'formations/ajout_chapitre.html',locals())
    else :
        raise Http404