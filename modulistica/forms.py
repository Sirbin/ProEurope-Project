from user.models import UserProfile
from django import forms
from registration.forms import RegistrationForm


class UploadFileForm(forms.Form):
    modulistica = forms.FileField(label='Aggiungi Modulistica', required=False,)





