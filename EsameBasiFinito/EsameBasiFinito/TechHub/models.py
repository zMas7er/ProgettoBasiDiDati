from django.db import models

class Utente(models.Model):
    ID_utente = models.CharField(max_length=50, unique=True)  # usato per il login
    password = models.CharField(max_length=100)               # obbligatoria
    email = models.EmailField(blank=True, null=True)          # opzionale

    def __str__(self):
        return self.ID_utente


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


