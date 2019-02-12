from django.contrib import admin
from cours.models import *

# Register your models here.

class FormationAdmin(admin.ModelAdmin):
    list_display = ('id' , 'formation_libelle' , 'formation_utilisateur' , 'formation_categorie')
    ordering = ('id' , 'formation_libelle' )
    search_fields = ('formation_libelle','formation_utilisateur')

class UtisAdmin(admin.ModelAdmin):
   list_display   = ('id','utilisateur_nom', 'utilisateur_prenom', 'user','utilisateur_statu','utilisateur_genre','user')
   ordering       = ('id','utilisateur_nom')
   search_fields  = ('utilisateur_nom', 'utilisateur_prenom')


admin.site.register(FormationsSuivis)
admin.site.register(Chapitres)
admin.site.register(Categories)
admin.site.register(Formations,FormationAdmin)
admin.site.register(Utilisateurs,UtisAdmin)
admin.site.site_header = 'Administration Educ-o'
#admin.site.register(Commentaires)