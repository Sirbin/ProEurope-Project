from django.db import models

from azienda.models import Company
from django.contrib.auth.models import Group

#Base
from user.models import UserProfile

#Esterno

from guardian.models import GroupObjectPermission



#monkey path
Group.add_to_class('description',models.CharField(verbose_name='Descrizione',max_length=120,default=""))



