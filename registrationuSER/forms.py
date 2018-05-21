from user.models import UserProfile
from django import forms
from registration.forms import RegistrationForm


class EmailFieldMixin(forms.EmailField):

    default_validators = []


class FormRegistrationMixin(forms.ModelForm):

      class Meta:

          model = UserProfile
          fields = ['username','email','password','first_name','last_name']
          exclude = '__all__'

          labels = {
              'email':'Indirizzo Email',
              'first_name':'Nome',
              'last_name':'Cognome',
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

                    }),'password':forms.PasswordInput(attrs={
                                                'class':'form-control',
                                                'placeholder':'Password'

                    }),'first_name':forms.TextInput(attrs={
                                               'class':'form-control',
                                               'placeholder':'Nome',

                    }),'last_name':forms.TextInput(attrs={
                                               'class':'form-control',
                                               'placeholder':'Cognome'

                    })
                    }



          error_messages = {'username': {
                                'invalid':"L'utente deve contenere valori validi",
                                'required':"Il campo non deve essere vuoto",
                                'unique':"L'utente è gia presente"
                            },'email': {
                                'invalid':"L'email inserita non è valida!",

                            },'first_name':{
                                'required': "Il campo non deve essere vuoto",
                            }
          }

      def clean_email(self):
            user_ = self.cleaned_data['email']
            utente = UserProfile.objects.filter(email__icontains=user_)
            if utente:
                    raise forms.ValidationError('Questo indirizzo email appartine ad un utente registrato')
            return user_



      def save(self,commit=True):
           '''
           L'untente che si registra tramite il pulsante 'registra'
           sarà salvato con active e staff su false, sara poi
           lo staff che si curera di completare la registrazione
           '''
           user = super(FormRegistrationMixin, self).save(commit=False)
           user.set_password(self.cleaned_data["password"])
           if commit:
              user.save()
              return user
           return super(FormRegistrationMixin,self).save()


class RegistraionFormMixin(RegistrationForm):


    class Meta:

          model = UserProfile
          fields = '__all__'