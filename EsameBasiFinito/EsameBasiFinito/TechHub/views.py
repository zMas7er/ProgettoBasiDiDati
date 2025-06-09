from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
from TechHub.models import Azienda
from TechHub.models import Componenti, Utente, Ordine, Recensione
import json


# shop/views.py

def login_view(request):
    if request.method == 'POST':
        ID_utente = request.POST.get('ID_utente', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            utente = Utente.objects.get(ID_utente=ID_utente, password=password)
            request.session['utente_id'] = utente.id
            return redirect('componenti')
        except Utente.DoesNotExist:
            messages.error(request, 'Credenziali errate.')

    return render(request, 'login.html')
def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        ID_utente = request.POST.get('ID_utente', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()

        if not password:
            messages.error(request, 'La password non può essere vuota.')
        elif Utente.objects.filter(ID_utente=ID_utente).exists():
            messages.error(request, 'ID utente già registrato.')
        else:
            utente = Utente(ID_utente=ID_utente, password=password, email=email or None)
            utente.save()
            messages.success(request, 'Registrazione completata.')
            return redirect('login')

    return render(request, 'register.html')

def componenti_view(request):
    componenti = Componenti.objects.all()
    categorie = ["GPU", "CPU", "RAM", "Scheda madre"]
    return render(request, 'componenti.html', {
        'componenti': componenti,
        'categorie': categorie
    })


def crea_ordine_view(request):
    if request.method == 'POST' and 'utente_id' in request.session:
        try:
            import json
            data = json.loads(request.body)
            componenti_ids = data.get('componenti_ids', [])

            if not componenti_ids:
                return JsonResponse({'success': False, 'error': 'Nessun componente selezionato.'})

            totale = 0
            componenti = []

            for comp_id in componenti_ids:
                comp = Componenti.objects.get(id=comp_id)
                totale += float(comp.prezzo)
                componenti.append(comp)

            # crea ordine con prezzo totale
            ordine = Ordine.objects.create(
                utente_id=request.session['utente_id'],
                stato='attesa',
                prezzo=totale
            )

            for comp in componenti:
                ordine.componenti.add(comp)

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Metodo non valido'})


def ordini_view(request):
    if 'utente_id' not in request.session:
        return redirect('login')

    ordini = Ordine.objects.filter(utente_id=request.session['utente_id']).order_by('-data_creazione')
    return render(request, 'ordini.html', {'ordini': ordini})

def recensione_view(request):
    if request.method == 'POST' and 'utente_id' in request.session:
        titolo = request.POST.get('titolo')
        testo = request.POST.get('testo')
        voto = request.POST.get('voto')

        if voto and int(voto) > 0:
            Recensione.objects.create(
                titolo=titolo,
                voto=int(voto),
                testo=testo,
                utente_id=request.session['utente_id']
            )
            messages.success(request, 'Recensione inviata con successo!')
        else:
            messages.error(request, 'Devi selezionare un voto.')

    return redirect('home')


def aziende_view(request):
    aziende = Azienda.objects.all()
    return render(request, 'aziende.html', {'aziende': aziende})

def recensioni_view(request):
    recensioni = Recensione.objects.all().order_by('-ID_recensione')
    return render(request, 'recensioni.html', {'recensioni': recensioni})

def chi_siamo_view(request):
    return render(request, 'chi_siamo.html')