# TECHHUB - PORTALE DI COMPONENTI TECNOLOGICI

TechHub è un sito web per acquistare e recensire componenti hardware come CPU, GPU, RAM e altro. Gli utenti possono registrarsi, fare ordini, lasciare recensioni con stelle e vedere le aziende partner.

---

## COME USARE IL SITO

### 1. HOME
- Pagina principale con tutti i pulsanti utili (login, registrazione, ordini, recensioni, aziende, info).
- Da qui puoi accedere a tutte le sezioni del sito.

### 2. REGISTRAZIONE
- Inserisci un ID univoco, password e email (opzionale).
- Se l’ID è già in uso, ricevi un messaggio d’errore.

### 3. LOGIN
- Inserisci ID e password.
- Dopo il login vieni reindirizzato alla pagina dei componenti.

### 4. COMPONENTI
- Vedi la lista dei componenti disponibili divisi per categoria.
- Puoi aggiungere prodotti al carrello e scegliere il metodo di pagamento.
- Dopo il pagamento, l’ordine viene salvato nel database.

### 5. ORDINI
- Mostra tutti gli ordini dell’utente attualmente loggato.

### 6. RECENSIONI
- Dalla home clicca su "Scrivi una recensione".
- Inserisci titolo, testo e clicca una delle 5 stelle.
- Dopo l’invio, la recensione è salvata nel database.
- Puoi vedere tutte le recensioni cliccando sulla stella in basso a destra nella homepage.

### 7. AZIENDE
- Pagina con tutte le aziende che forniscono i componenti.

### 8. ADMIN
- Accesso riservato agli admin da `/admin`.
- Richiede autenticazione.

---

## STRUTTURA DEL PROGETTO

### MODELLI (`models.py`)
- **Utente**: `ID_utente`, `password`, `email`
- **Azienda**: `ID_azienda`, `nome`, `sede_legale`
- **Componenti**: `nome`, `marca`, `tipologia`, `prezzo`, `immagine`, `ID_azienda`
- **Ordine**: `ID_ordine`, `utente`, `nome`, `stato`, `data_creazione`
- **Recensione**: `ID_recensione`, `titolo`, `voto (1-5)`, `testo`, `ID_utente`

### VISTE (`views.py`)
- `login_view`
- `register_view`
- `home_view`
- `componenti_view`
- `crea_ordine_view`
- `ordini_view`
- `recensione_view`
- `recensioni_view`
- `aziende_view`
- `chi_siamo_view`

### TEMPLATE HTML
- `home.html`
- `login.html`
- `register.html`
- `componenti.html`
- `ordini.html`
- `recensioni.html`
- `aziende.html`
- `chi_siamo.html`

---

## ISTRUZIONI DI AVVIO

1. Crea l’ambiente virtuale:
   ```bash
   python -m venv .venv
   ```

2. Attivalo:
   ```bash
   .venv\Scripts\activate
   ```

3. Installa i pacchetti:
   ```bash
   pip install django
   ```

4. Esegui le migrazioni:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Avvia il server:
   ```bash
   python manage.py runserver
   ```

6. Vai su:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

**Autore**: Gianmarco Montella
**Corso**: Basi di Dati
**Università**: Università degli studi di Napoli Parthenope