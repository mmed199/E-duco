from django.db import models
from datetime import date, datetime
import os
import unicodedata
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation
from .fields import OrderField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.


def file_name_utis(instance,filename):
    path = "uploads/utilisateurs/"
    concat = str(instance.id) + '_' + str(instance.utilisateur_nom).replace(' ','_') +'_'+str(instance.utilisateur_prenom).replace(' ','_') + '.' + filename.split('.')[-1]
    format = (unicodedata.normalize('NFKD', concat).encode('ascii', 'ignore')).decode("utf-8")

    if(os.path.isfile(os.path.join(path, format))):
        os.remove(os.path.join(path, format))
        return os.path.join(path, format)
    else:
        return os.path.join(path, format)
        
def file_name_formation(instance,filename):
    path = "uploads/formation/"
    concat = str(instance.formation_utilisateur).replace(' ','_') + '__' + str(instance.formation_libelle).replace(' ','_') +'.'+ filename.split('.')[-1]
    format = (unicodedata.normalize('NFKD', concat).encode('ascii', 'ignore')).decode("utf-8")

    if(os.path.isfile(os.path.join(path, format))):
        os.remove(os.path.join(path, format))
        return os.path.join(path, format)
    else:
        return os.path.join(path, format)   

def image_name_chapitre(instance,filename):
    path = "uploads/formation/media"
    concat = str(instance.course).replace(' ','_') + '/' + str(instance.titre).replace(' ','_') + '.' +filename.split('.')[-1]
    format = (unicodedata.normalize('NFKD', concat).encode('ascii', 'ignore')).decode("utf-8")
    if(os.path.isfile(os.path.join(path, format))):
            os.remove(os.path.join(path, format))
            return os.path.join(path, format)
    else:
            return os.path.join(path, format) 

def file_name_chapitre(instance,filename):
    path = "uploads/formation/media"
    concat = str(instance.course.formation_slug).replace('-','_') + '/fichier_' + str(instance.titre).replace(' ','_') + '.' +filename.split('.')[-1]
    format = (unicodedata.normalize('NFKD', concat).encode('ascii', 'ignore')).decode("utf-8")
    if(os.path.isfile(os.path.join(path, format))):
            os.remove(os.path.join(path, format))
            return os.path.join(path, format)
    else:
            return os.path.join(path, format) 
        
class Utilisateurs(models.Model):
    genre = [('H','Homme') , ('F','femme')]
    vouloir = [('E','Lancer des cours') , ('P','Chercher des cours'),('D','Les deux')]
    user = models.OneToOneField(User, on_delete = models.CASCADE )
    utilisateur_nom = models.CharField(max_length = 50,default='default',verbose_name = "Nom du utilisateur")
    utilisateur_prenom = models.CharField(max_length = 50,default='default',verbose_name = "Prenom du utilisateur")
    utilisateur_image = models.ImageField(upload_to = file_name_utis, default = 'uploads/default.png',verbose_name = "Image du utilisateur")
    utilisateur_statu = models.CharField(max_length= 150,default='default',verbose_name = "Statu Actuel du utilisateur")
    utilisateur_date_naissance = models.DateField(default = date.today,verbose_name = "Date de naissance du utilisateur")
    utilisateur_bio = models.TextField(default='',verbose_name = "Bio utilisateur")
    utilisateur_veut = models.CharField(max_length = 2 , choices = vouloir , default ='D' , verbose_name = 'L\'utilisateur veut ')
    utilisateur_code = models.IntegerField(default = 0,verbose_name = "nombre verification")
    utilisateur_genre = models.CharField(max_length = 1 , choices = genre , default = 'H',verbose_name = "Sexe du utilisateur" )

    

    class Meta:
        verbose_name = "utilisateur"
    
    def __str__(self):
        s = self.utilisateur_nom + ' ' + self.utilisateur_prenom
        return s


class Formations(models.Model):
    formation_libelle = models.CharField(max_length = 80,verbose_name = "Libelle du Formation")
#    formation_prix = models.PositiveSmallIntegerField(verbose_name = "Prix du Formation")
    formation_utilisateur = models.ForeignKey('Utilisateurs',on_delete = models.CASCADE, default = None)
    formation_categorie = models.ForeignKey('Categories',on_delete = models.CASCADE)
    formation_bio = models.TextField(default='')
    formation_image = models.ImageField(upload_to = file_name_formation ,default='uploads/formation/default.png')
    formation_slug = models.SlugField(max_length=200)
    ratings = GenericRelation(Rating, related_query_name='Formations')
    class Meta:
        verbose_name = "Formation"
    
    def __str__(self):
        return self.formation_libelle


    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.formation_slug = slugify(self.formation_libelle)

        super(Formations, self).save(*args, **kwargs)


class Categories(models.Model):
    categorie_nom = models.CharField(max_length = 40,verbose_name = "Nom du Categorie")

    class Meta:
        verbose_name = "Categorie"
    def __str__(self):
        return self.categorie_nom

class Chapitres(models.Model):
    course = models.ForeignKey(Formations, related_name='modules',on_delete = models.CASCADE)
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    image = models.ImageField(upload_to = image_name_chapitre ,blank=True, null=True) #
    url = models.URLField(blank=True, null=True)
    fichier = models.FileField(upload_to = file_name_chapitre ,blank=True, null=True)
    contenu = models.TextField(default='')
    class Meta:
        ordering = ['order']
        verbose_name = "Chapitre"

    def __str__(self):
        return '{} - {}'.format(self.order, self.titre)

class FormationsSuivis(models.Model):
    utilisateur = models.ForeignKey(Utilisateurs, related_name='formations_suivis',on_delete = models.CASCADE)
    formation = models.ForeignKey(Formations, related_name = 'utilisateurs',on_delete= models.CASCADE)
    chapitre = models.ForeignKey(Chapitres, related_name = 'utilisateurs' , on_delete = models.CASCADE)
    fini = models.BooleanField(default = False)
    class Meta:
        verbose_name = "Formation suivi"






