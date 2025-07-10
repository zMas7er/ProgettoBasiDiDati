from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone
from TechHub.models import Azienda
from TechHub.models import Componenti, Utente, Ordine, Recensione, Giveaway, Partecipa
import json
import random

def login_view(request):
    if request.method == 'POST':
        ID_utente = request.POST.get('ID_utente', '').strip()
        password = request.POST.get('password', '').strip()
        ruolo = request.POST.get('ruolo', '').strip()

        if not ruolo:
            messages.error(request, 'Seleziona un ruolo.')
            return redirect('login')

        try:
            utente = Utente.objects.get(ID_utente=ID_utente, password=password)
            if utente.ruolo != ruolo:
                messages.error(request, 'Ruolo errato per questo account.')
                return redirect('login')
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

from decimal import Decimal

def componenti_view(request):
    utente_id = request.session.get('utente_id')
    sconto = 0
    utente = None

    if utente_id:
        utente = Utente.objects.get(id=utente_id)
        if utente.ruolo == 'azienda':
            sconto = 10  # esempio: 10% di sconto

    componenti = Componenti.objects.all()
    categorie = Componenti.objects.values_list('tipologia', flat=True).distinct()

    for comp in componenti:
        if sconto > 0:
            comp.prezzo_scontato = round(comp.prezzo - (comp.prezzo * sconto / 100), 2)
        else:
            comp.prezzo_scontato = None

    return render(request, 'componenti.html', {
        'componenti': componenti,
        'categorie': categorie,
        'sconto': sconto,
        'utente': utente
    })



def crea_ordine_view(request):
    if request.method == 'POST' and 'utente_id' in request.session:
        try:
            data = json.loads(request.body)
            componenti_ids = data.get('componenti_ids', [])

            if not componenti_ids:
                return JsonResponse({'success': False, 'error': 'Nessun componente selezionato.'})

            utente = Utente.objects.get(id=request.session['utente_id'])
            sconto = 10 if utente.ruolo == 'azienda' else 0

            totale = 0
            componenti = []

            for comp_id in componenti_ids:
                comp = Componenti.objects.get(id=comp_id)
                prezzo = float(comp.prezzo)
                if sconto:
                    prezzo -= prezzo * (sconto / 100)
                totale += prezzo
                componenti.append(comp)

            ordine = Ordine.objects.create(
                utente=utente,
                stato='attesa',
                prezzo=totale,
                sconto_applicato=sconto,
                nome=componenti[0].nome,
                marca=componenti[0].marca,
                tipologia=componenti[0].tipologia
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

def scelta_registrazione_view(request):
    return render(request, 'scelta_registrazione.html')

def register_privato_view(request):
    if request.method == 'POST':
        ID_utente = request.POST.get('ID_utente', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()

        if not password:
            messages.error(request, 'La password non può essere vuota.')
        elif Utente.objects.filter(ID_utente=ID_utente).exists():
            messages.error(request, 'ID utente già registrato.')
        else:
            utente = Utente(
                ID_utente=ID_utente,
                password=password,
                email=email or None,
                ruolo='privato'
            )
            utente.save()
            messages.success(request, 'Registrazione completata.')
            return redirect('login')

    return render(request, 'register_privato.html')


def register_azienda_view(request):
    if request.method == 'POST':
        ID_utente = request.POST.get('ID_utente', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        partita_iva = request.POST.get('partita_iva', '').strip()

        if not password:
            messages.error(request, 'La password non può essere vuota.')
        elif Utente.objects.filter(ID_utente=ID_utente).exists():
            messages.error(request, 'ID utente già registrato.')
        else:
            utente = Utente(
                ID_utente=ID_utente,
                password=password,
                email=email or None,
                ruolo='azienda',
                partita_iva=partita_iva or None
            )
            utente.save()
            messages.success(request, 'Registrazione completata.')
            return redirect('login')

    return render(request, 'register_azienda.html')

def profilo_view(request):
    if 'utente_id' not in request.session:
        return redirect('login')

    utente = Utente.objects.get(id=request.session['utente_id'])

    if request.method == 'POST':
        if utente.ruolo == 'privato':
            utente.data_nascita = request.POST.get('data_nascita') or None
            utente.telefono = request.POST.get('telefono') or None
        elif utente.ruolo == 'azienda':
            utente.partita_iva = request.POST.get('partita_iva') or None
            utente.telefono_aziendale = request.POST.get('telefono_aziendale') or None

        utente.nazionalita = request.POST.get('nazionalita') or None
        utente.save()
        messages.success(request, 'Profilo aggiornato.')

        return redirect('componenti')  # <--- Ritorna alla pagina componenti

    return render(request, 'profilo.html', {'utente': utente})

def logout_view(request):
    logout(request)
    # Rimuove messaggi in sospeso
    list(messages.get_messages(request))
    return redirect('home')

from django.utils import timezone

def giveaway_view(request):
    giveaway = Giveaway.objects.last()
    partecipanti = Partecipa.objects.filter(giveaway=giveaway).count()

    # Calcola giorni alla scadenza
    scadenza_giorni = (giveaway.data_fine - timezone.now()).days if giveaway else 0

    # Gestione POST (già la tua)
    if request.method == 'POST' and 'utente_id' in request.session:
        utente_id = request.session['utente_id']
        email = request.POST.get('email')

        if Partecipa.objects.filter(utente_id=utente_id, giveaway=giveaway).exists():
            messages.error(request, 'Hai già partecipato.')
            return redirect('home')

        Partecipa.objects.create(utente_id=utente_id, giveaway=giveaway, email=email)
        messages.success(request, 'Partecipazione registrata!')
        return redirect('home')

    return render(request, 'giveaway.html', {
        'giveaway': giveaway,
        'partecipanti': partecipanti,
        'scadenza_giorni': scadenza_giorni,
    })


def scegli_vincitore(giveaway):
    partecipanti = Partecipa.objects.filter(giveaway=giveaway)
    if partecipanti.exists():
        vincitore = random.choice(partecipanti)
        return vincitore.email
    return None
