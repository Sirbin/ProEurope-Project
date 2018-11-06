from django import forms
#Base
from gruppi.models import Company
from user.models import UserProfile
from .models import ClientUserCompany
from client.validators import check_file_name
#External
from localflavor.it.forms import ITSocialSecurityNumberField,ITVatNumberField,ITZipCodeField,ITPhoneNumberField
from localflavor.it.it_region import REGION_PROVINCE_CHOICES
from multiselectfield import MultiSelectFormField

class pro(ITVatNumberField):
    pass
class clientForm(forms.ModelForm):


    tipologia_beneficiario = (
        ('1','Associazione'),
        ('2','Onlus'),
        ('3','Cosorzio'),
        ('4','Piccola-Media Impresa'),
        ('5','Grande Impresa'),
        ('6','Micro Impresa'),
        ('7','Ente Pubblico'),
        ('8','S.r.l.'),
        ('9','S.r.l.s.'),
        ('10','S.a.s.'),
        ('11','S.n.c.'),
        ('12','S.r.l.'),
        ('13','Altro'),
    )

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

    tipologia_richiesta_agevolazione = (
        ('1','Contributo a Fondo Perduto'),
        ('2','Finanziamento a Tasso Agevolato'),
        ('3','Garanzia '),
    )

    denominazione = forms.CharField(label='Nome Azienda*',max_length=255,widget=forms.TextInput(attrs={'class':'form-control','id':'state-success','for':'state-success'}))
    nome = forms.CharField(label='Nome',label_suffix='N',max_length=255,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    cognome = forms.CharField(label='Cognome',label_suffix='C',max_length=255,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    indirizzo = forms.CharField(label='Indirizzo*',max_length=255,widget=forms.TextInput(attrs={'class':'form-control'}))
    pec = forms.CharField(label='Pec*',max_length=150,widget=forms.TextInput(attrs={'class':'form-control'}))
    citta = forms.CharField(label='Città*',max_length=255,widget=forms.TextInput(attrs={'class':'form-control'}))
    comune = forms.ChoiceField(label='Provincia*',widget=forms.Select(attrs={'class':'select2-container form-control select2','id':'s2id_autogen1'}),choices=REGION_PROVINCE_CHOICES)
    cap = ITZipCodeField(label='C.a.p*',error_messages={'invalid':'Inserisci una C.a.p corretto','required': 'Il campo non può essere vuoto'},widget=forms.TextInput(attrs={'class':'form-control'}))
    piva = ITVatNumberField(label='Partita Iva*',error_messages={'invalid':'Inserisci un P.iva corretta','required':'Il campo non può essere vuoto'},widget=forms.TextInput(attrs={'class':'form-control'}))
    cf = ITSocialSecurityNumberField(label='Codice Fiscale*',error_messages={'invalid':'Inserisci un Cod.Fiscale corretto','required':'Il campo non può essere nullo'},widget=forms.TextInput(attrs={'class':'form-control'}))
    telefonoFisso1 = ITPhoneNumberField(label='Telefono*',widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
    cellulare1 =  ITPhoneNumberField(label='Telefono Cellulare',widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    fax = ITPhoneNumberField(label='Fax',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    data_ins = forms.DateTimeField(required=False,label='Data Registrazione',input_formats=('%d-%m-%Y %H:%M:%S',))
    data_mod = forms.DateTimeField(required=False,label='Data Utima Modifica',input_formats=('%d-%m-%Y %H:%M:%S',))
    email = forms.EmailField(max_length=150,label='Email*',widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'invalid':"L'email inserita non è valida!", 'required':'Il campo non può essere vuoto'})
    url_sito = forms.URLField(max_length=150,label='Sito Web',widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'invalid':"Sito Web inserito non è valido!"},required=False)
    note = forms.CharField(label='Note',max_length=500,widget=forms.Textarea(attrs={'class':'form-control'}),required=False)
    codice_ateco = forms.CharField(label='Codice Ateco*',max_length=150,widget=forms.TextInput(attrs={'class':'form-control'}))
    numero_rea = forms.CharField(label='Numero Rea*',max_length=150,widget=forms.TextInput(attrs={'class':'form-control'}))

    #Tipologia
    tipologia = forms.ChoiceField(choices=tipologia_beneficiario,label='Tipologia*',widget=forms.Select(attrs={'class':'form-control'}),required=False)
    tipologia_altro = forms.CharField(label='Altro',max_length=150,widget=forms.TextInput(attrs={'class':'form-control'}),required=False)

    #Comapagine Sociale
    numero_dipendenti = forms.IntegerField(min_value=0,max_value=2500,label='N.Dipendenti',widget=forms.NumberInput(attrs={'class':'form-control'}),required=False)
    meno_di_35  = forms.IntegerField(min_value=0,max_value=2500,label='N.Meno di 35',widget=forms.NumberInput(attrs={'class':'form-control'}),required=False)
    donna_uomo = forms.IntegerField(min_value=0,max_value=2500,label='N.Donna',widget=forms.NumberInput(attrs={'class':'form-control'}),required=False)
    donna_uomo_1 = forms.IntegerField(min_value=0,max_value=2500,label='N.Uomo',widget=forms.NumberInput(attrs={'class':'form-control'}),required=False)
    #Spese
    spese = MultiSelectFormField(max_choices=15,choices=select_spese,widget=forms.CheckboxSelectMultiple(),required=False)
    spese_altro = forms.CharField(label='Altre Spese', max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    note_1 = forms.CharField(label='Note',help_text='Fornire maggiorni dettagli sulle spese da sostenere, se necessario*',max_length=500,widget=forms.Textarea(attrs={'class':'form-control'}),required=False)
    tipologia_richiesta = forms.ChoiceField(choices=tipologia_richiesta_agevolazione,required=False,label='Quale tipologia di agevolazione è richiesta ?*',widget=forms.Select(attrs={'class':'form-control'}))
    #ProEurope
    Procedure_1 = forms.CharField(label='Attività preliminari che il beneficiario deve attuare',max_length=250,widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    Procedure_2 = forms.CharField(label='Attività preliminari che ProEurope deve attuare',max_length=250,widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    Procedure_3 = forms.CharField(label='Possibili bandi da valutare',max_length=250,widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    #Allegati
    doc = forms.FileField(label='Documento di Riconoscimento',required=False,validators=[check_file_name])
    cf_doc = forms.FileField(label='Codice Fiscale',required=False,validators=[check_file_name])
    attrribuzione_pi = forms.FileField(label='Attribuzione Partiva Iva',required=False,validators=[check_file_name])
    certificato_camerale = forms.FileField(label='Certificato Camerale',required=False,validators=[check_file_name])
    visura_camerale = forms.FileField(label='Visura Camerale',required=False,validators=[check_file_name])
    contratto = forms.FileField(label='Contratto Proprietà / Locazione',required=False,validators=[check_file_name])
    preventivi = forms.FileField(label='Preventivi / Fatture',required=False,validators=[check_file_name])
    mod_unico_anno_prec = forms.FileField(label='Modello unico precedente',required=False,validators=[check_file_name])
    mod_unico_anno_prec_2 = forms.FileField(label='Modello unico',required=False,validators=[check_file_name])
    bilancio_ultimi_2 = forms.FileField(label='Bilancio anno precedente',required=False,validators=[check_file_name])
    bilancio_anno_corso = forms.FileField(label='Situazione bilancio provvisoria',required=False,validators=[check_file_name])
    attestati = forms.FileField(label='Titoli abilitativi(attestati)',required=False,validators=[check_file_name])
    allegati_autocertificazione = forms.FileField(label='Allegati ed Autocertificazioni',required=False,validators=[check_file_name])
    altri_allegati = forms.FileField(label='Altri allegati',help_text='*Il file deve essere in formato compresso (zip o rar)',required=False,validators=[check_file_name])

    def clean_email(self):

        email = self.cleaned_data['email']
        email_check = ClientUserCompany.objects.exclude(email=self.instance.email).filter(email__iexact=email)
        if email_check:
            raise forms.ValidationError('Email gia esistente')
        return email

    def clean_piva(self):
        piva = self.cleaned_data['piva']
        p_iva_check = ClientUserCompany.objects.exclude(piva=self.instance.piva).filter(piva__iexact=piva)
        if p_iva_check:
            raise forms.ValidationError('Partita Iva già presente')
        return piva

    def clean_cf(self):
        cf = self.cleaned_data['cf']
        cf_check = ClientUserCompany.objects.exclude(cf=self.instance.cf).filter(cf__iexact=cf)
        if cf_check:
            raise forms.ValidationError('Codice Fiscale già presente')
        return cf

    def clean_denominazione(self):
        azienda = self.cleaned_data['denominazione']
        cf_azienda_check = ClientUserCompany.objects.exclude(denominazione=self.instance.denominazione).filter(denominazione__iexact=azienda)
        if cf_azienda_check:
            raise forms.ValidationError('Azienda già presente')
        return azienda



    class Meta:

        model = ClientUserCompany
        fields = '__all__'
        exclude = ['telefonoFisso2','cellulare2','data_ins','data_mod']


        widgets = {
            'user':forms.Select(attrs={
                                           'class':'form-control',
                                            'placeholder':'Seleziona Azienda',
            }),
        }



    # init inseriscilo sempre dopo della classe Meta
    def __init__(self, username,group, *args, **kwargs):
        '''
        Inserisce username(inviato da get_form_kwars) e controlla quale azienda è
        collegata con l'utente.
        questo per visualizzare nel ModelChoicheForm
        '''

        super(clientForm, self).__init__(*args, **kwargs)

        try:
            self.user_for_company = Company.objects.get(azienda_user__username=username)
            print(group)

            if group == 'Utente':
                self.fields['user'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(username=username),
                                                            widget=forms.Select(attrs={'class':'form-control'}))
            elif group == 'Administrator':
                self.fields['user'] = forms.ModelChoiceField(
                                     queryset=UserProfile.objects.filter(azienda__denominazione=self.user_for_company.denominazione),
                                              widget=forms.Select(attrs={'class':'form-control'})
        )
        except:
            self.fields['user'] = forms.ModelChoiceField(
                                     queryset=UserProfile.objects.all(),
                                              widget=forms.Select(attrs={'class':'form-control'} )
        )


class attachedClientForm(forms.Form):
    nome_allegato = forms.CharField(label='Nome Allegato',required=False, error_messages={'required':'Il campo non può essere vuoto'})
    allegato = forms.FileField(label='Aggiungi Allegato', required=True, error_messages={'required':'Il campo non può essere vuoto'},)






