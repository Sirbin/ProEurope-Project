from django.db import models
from django.conf import settings
# Create your models here.



class Company(models.Model):
    '''
    Tabella Azinda
    '''
    denominazione = models.CharField(max_length=150,verbose_name='Denominazione')
    indirizzo = models.CharField(max_length=250,verbose_name='Indirizzo')

    citta = models.CharField(max_length=150,verbose_name='Città')
    comune = models.CharField(max_length=100,verbose_name='Comune')
    cap = models.CharField(verbose_name='C.a.p.',max_length=20)
    piva = models.CharField(verbose_name='P.iva',max_length=14)
    cf = models.CharField(verbose_name='Codice Fiscale',max_length=16)
    telefonoFisso1 = models.CharField(verbose_name='Telfono', null=True,max_length=15)
    telefonoFisso2 = models.CharField(verbose_name='Telfono Altro', null=True,max_length=15)
    cellulare1 = models.CharField(verbose_name='Celluare',max_length=15)
    cellulare2 = models.CharField(verbose_name='Celluare Altro',max_length=15)
    url_sito = models.CharField(max_length=255)
    fax = models.CharField(verbose_name='Fax',max_length=15)
    email = models.CharField(verbose_name='E-mail',max_length=150)
    data_ins = models.DateTimeField('Data inserimento',auto_now=True)

    def __str__(self):
        return self.denominazione




    class Meta():

          permissions = (
            ("Can_View", "Può Visualizzare la Lista"),

        )


