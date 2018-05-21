from django.core.validators import ValidationError
from django.utils.translation import ugettext_lazy as _

def check_file_name(valore):

      '''
      Controlla che l'estensione del file sia 'jpg','xlsx','doc','pdf'

      '''
      exten = ('.jpg','.pdf','.xlsx','.doc','.docx','zip','rar','.PDF','.p7m')
      data = valore.name.endswith(exten)
      if not data:
            raise ValidationError(_('Il File %s non è Corretto'% valore.name),params={'valore':valore})
