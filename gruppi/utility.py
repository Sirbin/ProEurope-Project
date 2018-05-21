from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
create_C = ContentType.objects.get_for_model(Group)

perm = Permission.objects.create(codename='Can_View',name='Può Visualizzare i gruppi',content_type=create_C)
#perm_c = Permission.objects.get(name='Può Visualizzare')
#print(perm_c)