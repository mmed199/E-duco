"""site_pfe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('' , views.index,name= 'index'),
    path('inscription/',views.pre_inscription,name= 'pre_inscription'),
    path('recherche',views.recherche,name='recherche'),
    path('inscription/utilisateur',views.utilisateur_inscription,name= 'utilisateur_inscription'),
    url(r'^inscription/verification/(?P<id_utilisateur>[0-9])', views.verification, name= 'verification'),
    path('supprimer-chapitre/<str:id>/<int:formation_id>/<int:commit>',views.supprimer_chapitre, name='supprimer_chapitre'),
    path('supprimer-formation/<str:id>/<int:commit>',views.supprimer_formation, name='supprimer_formation'),
    path('ajout-formation',views.ajout_formation,name='ajout_formation'),
    path('ajout-formation/ajout-chapitres/<int:id>',views.ajout_chapitre, name = "ajout_chapitre"),
    path('next/<int:id>/<int:order>',views.next_chapitre, name = "next_chapitre"),
    path('cours',views.cours, name = 'cours'),
    path('cours/categories/<int:id_categorie>',views.cours_categorie,name = 'cours_par_categorie'),
    path('cours/recherche/<str:recherche>',views.cours_recherche, name = 'cours_recherche'),
    path('<int:id>/<slug:slug>',views.cours_display, name = 'cours_display'),
    path('<int:id>/<slug:slug>/<int:order>',views.chapitre_display, name = 'chapitre_display'),
    url(r'^connexion/$', auth_views.LoginView.as_view(template_name = "connexion/login.html"), name='login'),

    url(r'^deconnexion/$', auth_views.LogoutView.as_view(), name='logout' )
   # path('connexion', views.login, name='login'),
]

