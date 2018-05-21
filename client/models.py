from django.core.files.storage import FileSystemStorage,File
from django.db import models
from django.contrib import messages
from django.core.files import File
# Create your models here.
from user.models import UserProfile
from django.conf import settings
import os,zipfile
import shutil
#external
from multiselectfield import MultiSelectField




def for_id(instance,filename):

        return "{0}/{1}".format(instance.denominazione,filename)

class CreateFolderUser(FileSystemStorage):
    '''
    Gestione dei file
    '''

    path_create = os.path.join(os.path.dirname(settings.MEDIA_ROOT), 'media')

    path_create_zip = os.path.join(os.path.dirname(settings.TMP_ROOT), 'tmp')

    path_create_zip_proof = os.path.join(os.path.dirname(settings.ZIP_ROOT), 'zip')

    def create_zip_file(self,name):
        '''
        Creazione del file zip
        '''
        #if self.exists_file(name):
        if self.exists_file(name+'.zip'):
           #path =  os.path.join(os.path.dirname(settings.MEDIA_ROOT),'media')
           try:
            os.remove(os.path.join(self.path_create,name+'.zip'))
            #os.remove(os.path.join(path,name+'.zip'))
           except:
                pass
           #create_zipfile_for_client_def = zipfile.ZipFile(os.path.join(path, name+'.zip') ,'a',zipfile.ZIP_DEFLATED)
           #create_zipfile_for_client_def.write(path)
           create_zipfile_for_client_def = zipfile.ZipFile(os.path.join(self.path_create, name+'.zip') ,'a',zipfile.ZIP_DEFLATED)
           create_zipfile_for_client_def.write(self.path_create)
           for dirname,subdirs,files in os.walk(os.path.join(os.path.dirname(settings.MEDIA_ROOT) ,'media', name)):
                for filename in files:
                    create_zipfile_for_client_def.write(os.path.join(dirname,filename))
           create_zipfile_for_client_def.close()
        else:
           create_zipfile_for_client_def = zipfile.ZipFile(os.path.join(self.path_create, name + '.zip'), 'a',
                                                        zipfile.ZIP_DEFLATED)
           create_zipfile_for_client_def.write(self.path_create)
           for dirname, subdirs, files in os.walk(os.path.join(os.path.dirname(settings.MEDIA_ROOT), 'media', name)):
                for filename in files:
                    create_zipfile_for_client_def.write(os.path.join(dirname, filename))
           create_zipfile_for_client_def.close()


    def create_zip_file_altri_allegati(self,oby,name):

        if self.exists_file(name+'_altri_allegati'+'.zip'):
            print(self.exists_file(name+'_altri_allegati'+'.zip'))
            # gli facciamo creare il file zip direttamente su media
            create_zip_file = zipfile.ZipFile(os.path.join(self.path_create_zip_proof,name+'_altri_allegati'+'.zip'),'a',zipfile.ZIP_DEFLATED)
            print(create_zip_file)
            for files_name in oby:
                destination_save = open(os.path.join(self.path_create_zip,files_name.name),'wb+')
                for files in files_name.chunks():
                    destination_save.write(files)
                destination_save.close()
            for dirname,subdirs,files in os.walk(self.path_create_zip): #ilproblema è il loop
                for filename in files:
                   create_zip_file.write(os.path.join(dirname,filename))
            create_zip_file.close()
        else:
            print(self.exists_file(name + '_altri_allegati' + '.zip'))

            create_zip_file = zipfile.ZipFile(os.path.join(self.path_create_zip_proof, name+'_altri_allegati'+'.zip'),'a', zipfile.ZIP_DEFLATED)

            print(create_zip_file)

            for files_name in oby:
                destination_save = open(os.path.join(self.path_create_zip, files_name.name), 'wb+')
                for files in files_name.chunks():
                    destination_save.write(files)
                destination_save.close()
            for dirname, subdirs, files in os.walk(self.path_create_zip):
                for filename in files:
                    create_zip_file.write(os.path.join(dirname,filename))
            create_zip_file.close()

    def get_file_zip(self,name):

        for file in os.listdir(self.path_create_zip_proof):
                print('questo',file)
                print('vero',self.exists_file_zip(name+'_altri_allegati'+'.zip'))
                if self.exists_file_zip(name+'_altri_allegati'+'.zip'):
                    shutil.copy(os.path.join(self.path_create_zip_proof,file),os.path.join(self.path_create))
                    shutil.copy(os.path.join(self.path_create_zip_proof,file),os.path.join(self.path_create,name))
                    for file_delete in os.listdir(self.path_create_zip):
                        os.remove(os.path.join(self.path_create_zip,file_delete))
                    os.remove(os.path.join(self.path_create_zip_proof,file))
                    if self.listdir(self.path_create_zip_proof):
                        print(os.path.join(self.path_create,file))
                        return file

                return 'Errore ne copiare il file'
        return False


    def exists_file(self,name,name_zip=None):
        if name in os.listdir(os.path.join(os.path.dirname(settings.MEDIA_ROOT),'media')) or os.listdir(os.path.join(os.path.dirname(settings.TMP_ROOT),'tmp')) :
            return True
        return False

    def exists_file_zip(self, name, name_zip=None):
        if name in os.listdir(os.path.join(os.path.dirname(settings.ZIP_ROOT),'zip')):
            return True
        return False



    #def exists_file(self,name):
    #    if name in os.listdir(os.path.join(os.path.dirname(settings.MEDIA_ROOT),'media')):
    #        return True
    #    return False

    def create_folder(self,name=None):
        if not self.exists_file(name):
            create_folder = os.makedirs(os.path.join(os.path.dirname(settings.MEDIA_ROOT) ,'media', name))
            return create_folder
        return False

    def path(self, name):
        self._location = os.path.join(os.path.dirname(settings.MEDIA_ROOT) ,'media', name)
        return self._location

    def cancella_file(self,name,list_file=None):
        self.name = name
        self.list_file = list()
        if self.exists_file(self.name):
            for file in os.listdir(os.path.join(os.path.dirname(settings.MEDIA_ROOT),'media',self.name)):
                try:
                    os.remove((os.path.join(os.path.dirname(settings.MEDIA_ROOT),'media', self.name, file)))
                except:
                    raise

    def size(self, name):
        return super(CreateFolderUser,self).size(name)

    def get_modified_time(self, name):
        return super(CreateFolderUser,self).size(name)

class documentFile(models.Model):

      name = models.CharField(max_length=100)
      docFile = models.FileField(blank=True)

      def __str__(self):
          return self.name


class ClientUserCompany(models.Model,CreateFolderUser):

    select_spese = (
        ('1','Avvio Attività'),
        ('2','Attrezzature e Macchinari'),
        ('3','Opere Edili e Impianti(Costruzione'),
        ('4','Opere Edili e Impianti(Ristrutturazione)'),
        ('5','Opere Edili e Impianti(Ampliamento)'),
        ('6','Cosulenze/Servizi'),
        ('7','Acquisto Terreno'),
        ('8','Innovazione Ricerca e Sviluppo'),
        ('9','Risparmio Energetico/Fonti Rinnovabili'),
        ('10','Promozione/Export'),
        ('11','Realizzazione Sito Web'),
        ('12','Altro'),
    )

    denominazione = models.CharField(verbose_name='Denominazioe Ditta',max_length=255)
    is_complete = models.BooleanField(verbose_name="Pratica Comletata", default=False)
    ditta = models.BooleanField(verbose_name="Società",default=True)
    nome = models.CharField(verbose_name='Nome',max_length=150)
    cognome = models.CharField(verbose_name='Cognome',max_length=150)
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
    pec = models.CharField(verbose_name='pec',max_length=150)
    codice_ateco = models.CharField(verbose_name='Codice Ateco',max_length=150,default="")
    numero_rea = models.CharField(verbose_name='Numero Rea',max_length=150,default="")

    #date
    data_ins = models.DateTimeField('Data inserimento',auto_now_add=True)
    data_mod = models.DateTimeField('Data ultima modifica',auto_now=True)
    note = models.CharField(verbose_name='Note',max_length=255)
    user = models.ForeignKey(UserProfile,related_name='user_for_client',null=True)
    # tipologia
    tipologia = models.CharField(verbose_name='Tipologia',max_length=100)
    tipologia_altro = models.CharField(verbose_name='Altro',max_length=150,default="")
    # compagine sociale
    numero_dipendenti = models.CharField(verbose_name='Numero Dipendenti',max_length=15,default=0,null=True)
    meno_di_35  = models.CharField(verbose_name='Meno di 35',max_length=15,default=0,null=True)
    donna_uomo = models.CharField(verbose_name='Uomo',max_length=50,default=0,null=True)
    donna_uomo_1 = models.CharField(verbose_name='Donna',max_length=50,default=0,null=True)
    # Domande Finanziamento
    spese = MultiSelectField(choices=select_spese)
    spese_altro = models.CharField(verbose_name='Altre Spese',max_length=150,default="")
    note_1 = models.CharField(verbose_name='Dettaglio Spese',max_length=500)
    tipologia_richiesta = models.CharField(verbose_name='Tipologia Spese',max_length=50)
    #Solo ProEurope Procedure

    Procedure_1 = models.CharField(max_length=155)
    Procedure_2 = models.CharField(max_length=155)
    Procedure_3 = models.CharField(max_length=155)

    #Allegati


    fs = CreateFolderUser(location=for_id,directory_permissions_mode=None)


    doc = models.FileField(blank=True,storage=fs,upload_to=for_id)#
    cf_doc = models.FileField(blank=True,storage=fs,upload_to=for_id)
    attrribuzione_pi = models.FileField(blank=True,storage=fs,upload_to=for_id)#
    certificato_camerale = models.FileField(blank=True,storage=fs,upload_to=for_id)
    visura_camerale = models.FileField(blank=True,storage=fs,upload_to=for_id)
    contratto = models.FileField(blank=True,storage=fs,upload_to=for_id)
    preventivi = models.FileField(blank=True,storage=fs,upload_to=for_id)
    mod_unico_anno_prec = models.FileField(blank=True,storage=fs,upload_to=for_id)
    mod_unico_anno_prec_2 = models.FileField(blank=True,storage=fs,upload_to=for_id)
    bilancio_ultimi_2 = models.FileField(blank=True,storage=fs,upload_to=for_id)
    bilancio_anno_corso = models.FileField(blank=True,storage=fs,upload_to=for_id)
    attestati = models.FileField(blank=True,storage=fs,upload_to=for_id)#
    allegati_autocertificazione = models.FileField(blank=True,storage=fs,upload_to=for_id)
    altri_allegati = models.FileField(blank=True,storage=fs,upload_to=for_id)

    def __str__(self):
        return self.denominazione

    @property
    def is_completated(self):
        if self.is_complete:
            return True
        return False


    class Meta():

        permissions = (
            ("Can_View", "Può Visualizzare i Clienti"),
            ("Can_Password", "Può Modificare la Password"),
            ("Can_Down",'Può Scaticare allegati'),
            ("Can_View_att",'Può Visualizzare allegati'),
        )