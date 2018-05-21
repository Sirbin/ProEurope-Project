from django import forms
#Base
from user.models import Permission,Group




class formGroups(forms.ModelForm):

    '''
    Form per i permessi di gruppo,
    impostiamo labels,widgets
    '''

    permissions = forms.ModelMultipleChoiceField(label='Permessi Gruppi',queryset=Permission.objects.all(),required=False,widget=forms.SelectMultiple(attrs={'size':30,'class':'form-control'}))

    class Meta():

        model = Group
        fields = '__all__'

        labels = {
              'name':'Nome',
              'description':'Descrizione Gruppo',
        }

        widgets = {
               'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Nome'}),
               'description':forms.TextInput(attrs={'class':'form-control','placeholder':'Descrizione'}),
                   }