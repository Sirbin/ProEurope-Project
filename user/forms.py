#Django
from django.core.validators import ValidationError,EmailValidator
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm,SetPasswordForm
#Base
from user.models import UserProfile,Permission,Group
from django import forms
#External

from django.utils.translation import ugettext_lazy as _

class EmailFieldMixin(forms.EmailField):

    default_validators = []

class FormPassChange(PasswordResetForm):

   email = EmailFieldMixin(max_length=100,label='Email',
                                    widget=forms.TextInput(attrs={
                                   'class':'form-control',
                                   'placeholder':'Inserisci E-mail',
                               }),validators=[EmailValidator(message="L'E-mail inserita non è valida!")])

   def clean_email(self):
        user_ = self.cleaned_data['email']
        if UserProfile.objects.filter(email__icontains=user_):
            return user_
        else:
            raise forms.ValidationError('Questo indirizzo email non appartiene a nessun utente registrato')

class FormLogin(AuthenticationForm):

    username = forms.CharField(max_length=254,min_length=4,
                               widget=forms.TextInput(attrs={
                                   'class':'form-control',
                                   'placeholder':'Username',
                                   'id':'alloptions',
                                   'name':'alloptions'
                               }))

    password = forms.CharField(min_length=8,
                               widget=forms.PasswordInput(attrs={
                                   'class':'form-control',
                                   'placeholder':'Password',
                               }))

class SetPassword(SetPasswordForm):

    error_messages = {'password_mismatch':_('Le passoword non coincidono')}

    new_password1 = forms.CharField(min_length=8,
                                    widget=forms.PasswordInput(attrs={
                                   'class':'form-control',
                                   'placeholder':'Inserisci Password',
                                    }))

    new_password2 = forms.CharField(min_length=8,
                                    widget=forms.PasswordInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Rinserisci Password',
                                    }))


class ChangePasswordUser(SetPasswordForm):

       new_password1 = forms.CharField(min_length=8,label=' Nuova Password',
                                    widget=forms.PasswordInput(attrs={
                                   'class':'form-control',
                                   'placeholder':'Inserisci Password',
                                    }))

       new_password2 = forms.CharField(min_length=8,label='Conferma Nuova Password',
                                    widget=forms.PasswordInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Rinserisci Password',
                                    }))

       def clean_new_password2(self):

            pass1 = self.cleaned_data['new_password1']
            pass2 = self.cleaned_data['new_password2']
            if pass1 != pass2:
                raise forms.ValidationError('Le Password non coincidono')
            return pass1



       class Meta():

           error_messages = {
                    'old_password': {'password_incorrect':
                                        "La Password è incorretta.",
                                    'required':'Il campo non può essere vuoto',

                                    }
           }

class UserFormEdit(forms.ModelForm):


    '''
    Form che Eredita parte del form di registrazione,
    inserisci tutti i campi del formdeglu utenti,
    vengono controllati la validità di tutti i form
    '''

    last_login = forms.DateTimeField(label='Ultimo Login',input_formats=('%d-%m-%Y %H:%M:%S',),
                                     widget=forms.DateTimeInput(attrs={'class':'form-control'},format='%d-%m-%Y %H:%M:%S'),
                                     error_messages={'invalid':'Inserisci una Data corretta'},
                                     help_text=" formato :'dd-mm-aaaa h:m:s",required=False)

    date_joined = forms.DateTimeField(label='Data Registrazione',input_formats=('%d-%m-%Y %H:%M:%S',),
                                      widget=forms.DateTimeInput(attrs={'class':'form-control'},format='%d-%m-%Y %H:%M:%S'),
                                      error_messages={'invalid':'Inserisci una Data corretta'},
                                      help_text=" formato :'dd-mm-aaaa h:m:s",required=False)



    #user_permissions = forms.ModelMultipleChoiceField(label='Permessi Utente',queryset=Permission.objects.all(),required=False,widget=forms.SelectMultiple(attrs={'class':'form-control'}))

    groups = forms.ModelMultipleChoiceField(label='Gruppi',queryset=Group.objects.all(),required=False,widget=forms.SelectMultiple(attrs={'class':'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        username_check = UserProfile.objects.exclude(username=self.instance.username).filter(username__iexact=username)
        if username_check:
            raise forms.ValidationError('Utente già presente')
        return username

    class Meta():

       model = UserProfile
       fields = '__all__'
       exclude = ['password','username']



       labels = {
              'email':'Indirizzo Email*',
              'first_name':'Nome*',
              'last_name':'Cognome*',
              'is_superuser':'Super Utente',
              'password':'Password*',
              'username':'Username*',
              'ripetipassword':'Ripeti Password*',
              'azienda':'Azienda*'

          }
       help_texts = {
             'is_superuser':"Se selezionato l'utente ha poteri Amministrativi",
             'is_staff':"Se selezionato l'utente puo accedere alla pagina Admin",
             'is_active':"Se selezionato l'utente è disattivato",

       }
       max_length = {
              'email':50
          }


       widgets = {'username':forms.TextInput(attrs={
                                               'class':'form-control',
                                               'placeholder':'Username'

                 }),'email':forms.TextInput(attrs={
                                               'class':'form-control',
                                               'placeholder':'Email',

                 }),'note':forms.Textarea(attrs={'class':'form-control',


                 }),'password':forms.PasswordInput(attrs={
                                                'class':'form-control',
                                                'placeholder':'Password'

                 }),'first_name':forms.TextInput(attrs={
                                               'class':'form-control',
                                               'placeholder':'Nome',

                 }),'last_name':forms.TextInput(attrs={
                                               'class':'form-control',
                                               'placeholder':'Cognome'

                 }),'azienda':forms.Select(attrs={
                                           'class':'form-control',
                                            'placeholder':'Seleziona Azienda'
                 }),'telefono':forms.TextInput(attrs={
                                           'class':'form-control',
                                           'placeholder':'Numero di Telefono'

                 }),'user_permissions': forms.SelectMultiple(attrs={
                                           'class':'form-control',
                                           'placeholder':'Permessi Utente'

                 }),


       }

       error_messages = {'username': {
                               'invalid':"Utente deve contenere valori validi",
                               'required':"Il campo non può essere vuoto",
                               'unique':"Utente gia presente"
                            },'email': {
                                'invalid':"L'email inserita non è valida!",
                                'required':'Il campo non può essere vuoto'
                            },'first_name':{
                                'required': "Il campo non può essere vuoto",
                            },'last_name':{
                                'required':"Il campo non può essere vuoto"
                            }
                        }


class UserFormAdd(UserFormEdit):

    new_password2 = forms.CharField(min_length=8,label='Ripeti Password*',
                                    widget=forms.PasswordInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Rinserisci Password',
                                    }))




    def clean_new_password2(self):
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['new_password2']
        if pass1 and pass2:
            if pass1 != pass2:
                raise ValidationError('Le Password non coincidono',code='password mismach')
            return pass1

    def save(self, commit=True):
        user = super(UserFormAdd, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta(UserFormEdit.Meta):

        fields = '__all__'
        exclude = ['']

class profileEdit(UserFormEdit):


    class Meta(UserFormEdit.Meta):


        fields = ['first_name','last_name','email','telefono','note']