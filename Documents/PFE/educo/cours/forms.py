from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class preInscriptionForm(forms.Form):
    in_email = forms.EmailField(widget = forms.EmailInput(attrs={'placeholder': 'exemple@email.exemple'}), label='E-mail ')
    in_mdp = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': '***********'}), label='Mot de passe ')
    in_re_mdp = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': '***********'}), label='Confirmation ')
    in_compte = forms.ChoiceField(choices = [('E','Lancer des cours') , ('P','Chercher des cours'),('D','Les deux')], widget=forms.Select())


class inscriptionUtilisateur(forms.Form):
    genre = [('H','Homme') , ('F','femme')]
    in_email = forms.CharField(widget = forms.HiddenInput())
    in_mdp = forms.CharField(widget = forms.HiddenInput() )
    in_compte = forms.CharField(widget = forms.HiddenInput() )
    in_nom = forms.CharField(widget = forms.TextInput(attrs = {'maxlength' : '15' , 'placeholder' : 'Nom de famille' , 'required' : 'required'}))
    in_prenom = forms.CharField(widget = forms.TextInput(attrs = {'maxlength' : '15' , 'placeholder' : 'Votre prènom' , 'required' : 'required'})) 
    in_genre = forms.ChoiceField(choices = genre, widget=forms.Select())
    in_date_naissance = forms.DateField( widget=forms.SelectDateWidget( years = range(1910,2000), empty_label=('1999','janvier','1') ) )
    in_statu = forms.CharField(widget = forms.TextInput(attrs = {'placeholder' : 'ex: Etudiant' , 'required' : 'required'}))   


class verificationForm(forms.Form):
    in_code = forms.IntegerField(max_value=9999 , min_value=1111)

class rechercheForm(forms.Form):
    order = [('C','Categories'), ('P' , 'Prix') , ('N' , 'Nom' ), ('D' , 'Date')]
    input_recherche = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'Recherche ...','id':'input-recherche'}))
    input_order = forms.ChoiceField(choices = order , widget = forms.Select(), required = False)


class ConnexionForm(forms.Form):
    username = forms.CharField(widget = forms.EmailInput(attrs={'placeholder': 'exemple@email.exemple','id':'mail'}), label='E-mail ')
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'placeholder': '***********','id':'mot-de-passe'}))



class ajoutFormation(forms.ModelForm):
    class Meta:
        model = Formations
        fields = ['formation_libelle' , 'formation_categorie' , 'formation_bio' , 'formation_image' ]

class ajoutChapitres(forms.ModelForm):
    class Meta:
        model = Chapitres
        fields = ['titre' , 'description'  ,'url','image', 'contenu', 'fichier']
