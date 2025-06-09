from django.contrib import admin
from .models import Utente, Azienda, Componenti, Ordine, Recensione

admin.site.register(Utente)
admin.site.register(Azienda)
admin.site.register(Componenti)
admin.site.register(Ordine)
admin.site.register(Recensione)
