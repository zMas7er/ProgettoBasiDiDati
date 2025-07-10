from django.db import models
from django.utils import timezone
from datetime import timedelta

class Utente(models.Model):
    RUOLO_CHOICES = [
        ('privato', 'Utente Privato'),
        ('azienda', 'Azienda'),
    ]

    ID_utente = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    ruolo = models.CharField(max_length=10, choices=RUOLO_CHOICES)

    # Dati per utenti privati
    data_nascita = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    # Dato comune
    nazionalita = models.CharField(max_length=50, blank=True, null=True)

    # Dati per aziende
    partita_iva = models.CharField(max_length=50, blank=True, null=True)
    telefono_aziendale = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.ID_utente} ({self.ruolo})"


class Azienda(models.Model):
    ID_azienda = models.AutoField(primary_key=True)
    nome_azienda = models.CharField(max_length=100, unique=True)
    sede_legale = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_azienda


class Componenti(models.Model):
    nome = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    tipologia = models.CharField(max_length=50)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    immagine = models.URLField(max_length=500, blank=True, null=True)
    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE, related_name='componenti')

    def __str__(self):
        return f"{self.nome} - {self.tipologia}"


class Ordine(models.Model):
    ID_ordine = models.AutoField(primary_key=True)
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='ordini')
    data_creazione = models.DateTimeField(auto_now_add=True)
    componenti = models.ManyToManyField(Componenti)
    stato = models.CharField(max_length=20, choices=[
        ('attesa', 'In attesa'),
        ('spedito', 'Spedito'),
        ('consegnato', 'Consegnato'),
        ('annullato', 'Annullato'),
    ])
    sconto_applicato = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    # Dati copiati dal componente
    nome = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    tipologia = models.CharField(max_length=50)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ID_ordine} - {self.nome} ({self.utente})"


class Recensione(models.Model):
    ID_recensione = models.AutoField(primary_key=True)
    titolo = models.CharField(max_length=100, default="")
    voto = models.IntegerField()
    testo = models.TextField()
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='recensioni')

    def __str__(self):
        return f"{self.titolo} ({self.voto} stelle)"

def default_data_fine():
    return timezone.now() + timedelta(days=7)

class Giveaway(models.Model):
    ID_giveaway = models.AutoField(primary_key=True)
    titolo = models.CharField(max_length=100)
    immagine = models.URLField()
    data_inizio = models.DateTimeField(default=timezone.now)
    data_fine = models.DateTimeField(default=default_data_fine)

    def __str__(self):
        return self.titolo


class Partecipa(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    email = models.EmailField()
    giveaway = models.ForeignKey(Giveaway, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utente', 'giveaway')

    def __str__(self):
        return f"{self.utente} - {self.email} - {self.giveaway}"
