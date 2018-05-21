from django.db import models
from azienda.models import Company
from django.contrib.auth.models import Group,Permission,UserManager,User,AbstractBaseUser,AbstractUser,BaseUserManager

# Create your models here.






class UserProfileManager(models.Manager):

       def get_last_login_value(self,username):
           get_value_last_login = self.filter(username=username).get('last_login')
           return get_value_last_login


class UserProfile(AbstractUser):
    '''
    Aggiunta di campi al model User, abbiamo cambiato anche 'AUTH_USER_MODEL'
    (vedi setting).

    aggiunto il campo note ,telefono , foto.
    aggiunto ancHeil campo azienda.
    '''



    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)

    user_permissions = models.ManyToManyField(Permission,verbose_name= 'Permessi Utente',blank=True,related_name="user_permissions_set")
    note = models.CharField(verbose_name='note',max_length=100,blank=True,null=True) # da cambiare
    telefono = models.CharField(verbose_name='Telefono',max_length=100,blank=True,null=True)
    imagineFoto = models.ImageField(upload_to='/media',blank=True,null=True)
    azienda = models.ForeignKey(Company,related_name='azienda_user',null=True,blank=True)
    prima_volta = models.BooleanField(verbose_name='Primo_login',default=False)


    def __str__(self):
        return self.first_name+' '+self.last_name

    #old Model
    #objects = models.Model()
    # new model with filter
    #user_azeinda = UserProfileManager()

    def get_groups(self,obj=None):
        '''
        Ritorna il gruppo relativo all'utente
        '''
        get_groups_by_name = UserProfile.objects.get(groups__id=1,username=self.username)

        return get_groups_by_name

    def clean_imagineFoto(self):
        pass

    def get_full_name(self):
        return self.first_name +" "+  self.last_name


    class Meta():

        permissions = (
            ("Can_View", "Può Visualizzare la Lista"),
            ("Can_Password", "Può Modificare la Password")
        )