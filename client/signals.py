
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

#Base
from .models import ClientUserCompany,CreateFolderUser
#External
import uuid
import datetime


# @receiver(pre_save,sender=ClientUserCompany)
# def create_folder(sender,instance,**kwargs):
#     print ('instance',instance)
#     print('k',kwargs)
#     f = ClientUserCompany()
#     f.create_folder(name=str(instance))