#Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
#Base
from .models import Company
#External
from localflavor.it.forms import ITProvinceSelect,ITRegionProvinceSelect,ITRegionSelect,\
                                 ITSocialSecurityNumberField,ITVatNumberField,ITZipCodeField,ITPhoneNumberField
from localflavor.it.it_region import REGION_CHOICES,REGION_PROVINCE_CHOICES



class prova(ITPhoneNumberField):
    pass


class AziendaForm(forms.ModelForm):

    '''
    Model Aziendale
    Tutti i campi sono controllati tramite error_message('da rivedere')
    # nelcaso ci fosse bisogno di altri campi
    '''

    denominazione = forms.CharField(label='Nome Azienda*',max_length=255,widget=forms.TextInput(attrs={'class':'form-control'}))
    indirizzo = forms.CharField(label='Indirizzo*',max_length=255,widget=forms.TextInput(attrs={'class':'form-control'}))
    citta = forms.CharField(label='Città*',max_length=255,widget=forms.TextInput(attrs={'class':'form-control'}))
    comune = forms.ChoiceField(label='Provincia*',widget=forms.Select(attrs={'class':'select2-container form-control select2','id':'s2id_autogen1'}),choices=REGION_PROVINCE_CHOICES)
    cap = ITZipCodeField(label='C.a.p*',error_messages={'invalid':'Inserisci una C.a.p corretto','required': 'Il campo non può essere vuoto'},widget=forms.TextInput(attrs={'class':'form-control'}))
    piva = ITVatNumberField(label='Partita Iva*',error_messages={'invalid':'Inserisci un P.iva corretta','required':'Il campo non può essere vuoto'},widget=forms.TextInput(attrs={'class':'form-control'}))
    cf = ITSocialSecurityNumberField(label='Codice Fiscale*',error_messages={'invalid':'Inserisci un Cod.Fiscale corretto','required':'Il campo non può essere nullo'},widget=forms.TextInput(attrs={'class':'form-control'}))
    telefonoFisso1 = ITPhoneNumberField(label='Telfono*',widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    #telefonoFisso2 = ITPhoneNumberField(label='Telefono Altro',help_text='Inserisc il Tel. con prefisso +39',widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    cellulare1 =  ITPhoneNumberField(label='Telefono Cellulare',widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    #cellulare2 = ITPhoneNumberField(label='Telefono Cellulare Altro',widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Inserisc il Tel. con prefisso +39',required=False)
    fax = ITPhoneNumberField(label='Fax',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    data_ins = forms.DateTimeField(required=False,label='Data Registrazione')
    email = forms.EmailField(max_length=150,label='Email*',widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'invalid':"L'email inserita non è valida!", 'required':'Il campo non può essere vuoto'})
    url_sito = forms.URLField(max_length=150,label='Sito Web',widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'invalid':"Sito Web inserito non è valido!"},required=False)

    class Meta:
        model = Company
        exclude = ['telefonoFisso2','cellulare2']
        fields = '__all__'

    # Controllo su i campi Principali

    def clean_email(self):

        email = self.cleaned_data['email']
        email_check = Company.objects.exclude(email=self.instance.email).filter(email__iexact=email)
        if email_check:
            raise forms.ValidationError('Email gia esistente')
        return email

    def clean_piva(self):
        piva = self.cleaned_data['piva']
        p_iva_check = Company.objects.exclude(piva=self.instance.piva).filter(piva__iexact=piva)
        if p_iva_check:
            raise forms.ValidationError('Partita Iva già presente')
        return piva

    def clean_cf(self):
        cf = self.cleaned_data['cf']
        cf_check = Company.objects.exclude(cf=self.instance.cf).filter(cf__iexact=cf)
        if cf_check:
            raise forms.ValidationError('Codice Fiscale già presente')
        return cf

    def clean_denominazione(self):
        azienda = self.cleaned_data['denominazione']
        cf_azienda_check = Company.objects.exclude(denominazione=self.instance.denominazione).filter(denominazione__iexact=azienda)
        if cf_azienda_check:
            raise forms.ValidationError('Azienda già presente')
        return azienda

class AziendaEdit(AziendaForm):

    '''
    Erdita la classe AziendaForm
    vengono sovrascritti vari controlli che non restituiscono nessun errore se fosse prensete il dato nel db
    gli altri controllo sono necessari
    '''
    class Meta(AziendaForm.Meta):

        model = Company

    
    def save(self, commit=True):
        azi = super(AziendaEdit, self).save(commit=False)
        if commit:
            azi.save()
        return azi
