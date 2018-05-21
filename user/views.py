#Django
from django.core.urlresolvers import reverse_lazy,reverse
from django.contrib.auth.mixins import PermissionRequiredMixin,PermissionDenied,LoginRequiredMixin
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import redirect_to_login
from django.views.generic import View,TemplateView,CreateView,ListView,UpdateView,DeleteView,FormView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
#Base
from user.models import UserProfile
from user.forms import UserFormEdit,UserFormAdd,profileEdit,ChangePasswordUser
from client.models import ClientUserCompany
from azienda.models import Company

import datetime


class prova(TemplateView,PermissionDenied):
      '''
      Semplice Prova da Cancellare
      '''
      login_url = reverse_lazy('userManagement')

      template_name = 'base/index.html'

      permission_denied_message = 'Errore'

      permission_required = 'is_staff'

      def get_context_data(self, **kwargs):
          contenxt = super(prova,self).get_context_data(**kwargs)
          contenxt['userlog'] = UserProfile.get_username(self.request.user)
          return contenxt

@login_required()
def dashboard(request):
    '''
    DashBoard deve essere differente per tipologi di utente
    '''
    template = 'base/index.html'
    context = {}
    context['time'] = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    userlog = UserProfile.get_username(request.user)
    messages.success(request,'Benvenuto Utente %s' % (userlog))
    return render(request,template, context)

class getFilterUserMixin(object):

    '''
    Mixin per recuperare le liste degli utenti in base all'azineda di appartenenza
    da utilizzare per ogni lista.
    '''

    def get_queryset(self):
         if not self.request.user.is_superuser:
            user_for_company = Company.objects.get(azienda_user__username=self.request.user.username)
            user_for_azi = UserProfile.objects.filter(azienda__denominazione=user_for_company.denominazione).exclude(username=self.request.user.username)
            print(user_for_azi)
            return user_for_azi
         return super(getFilterUserMixin,self).get_queryset()

class DashboardUser(LoginRequiredMixin,getFilterUserMixin,ListView):

        '''
        Pagina Princiapale
        '''

        model = ClientUserCompany

        userlog = ""

        permission_login_denied_message = 'Devi Prima Effettuare Il Login'

        permission_denied_message = "L'utente non ha i Permessi Necessari"

        template_name = 'base/index.html'

        def set_userLog(self):
            userlof = UserProfile.get_username(self.request.user)
            setattr(self.userlog,userlof)
            return self.userlog

        def get_context_data(self, **kwargs):
            '''
            Ritorna il numero di allegati che sono presenti per signolo utente
            '''
            clienti_user = super(DashboardUser,self).get_context_data(**kwargs)

            try:
                self.total = list(ClientUserCompany.objects.values('doc','cf_doc','attrribuzione_pi','certificato_camerale','visura_camerale',\
                'contratto','preventivi','mod_unico_anno_prec','mod_unico_anno_prec_2',\
                'bilancio_ultimi_2','bilancio_anno_corso','attestati','allegati_autocertificazione','altri_allegati')[0]).__len__()
            except:
                self.total = 0

            for azienda_denominazione in ClientUserCompany.objects.all():
                self.cli2 = ClientUserCompany.objects.values('doc','cf_doc','attrribuzione_pi','certificato_camerale','visura_camerale',\
                'contratto','preventivi','mod_unico_anno_prec','mod_unico_anno_prec_2',\
                'bilancio_ultimi_2','bilancio_anno_corso','attestati','allegati_autocertificazione','altri_allegati').get(denominazione= azienda_denominazione.denominazione)
                kwargs[azienda_denominazione.denominazione] = list(j for j in self.cli2 if self.cli2.get(j)).__len__()

            clienti_user['numero_allegati'] = kwargs
            clienti_user['totali'] = self.total
            return clienti_user

        def get_queryset(self):
            if not self.request.user.is_superuser:
                if not self.request.user.is_staff:
                    user_for_exclude = UserProfile.objects.all().values_list('username',flat=True).exclude(username=self.request.user.username)
                    user_for_company = Company.objects.get(azienda_user__username=self.request.user.username)
                    user_for_azi = ClientUserCompany.objects.filter(user__azienda__denominazione=user_for_company.denominazione).exclude(user__username__in=user_for_exclude)
                    return user_for_azi
                user_for_company = Company.objects.get(azienda_user__username=self.request.user.username)
                user_for_azi = ClientUserCompany.objects.filter(user__azienda__denominazione=user_for_company.denominazione)
                return user_for_azi
            return super(DashboardUser,self).get_queryset()

class AdminPermissionMixin(PermissionRequiredMixin):

    '''
    Minxin Globale per ogni model del app
    '''

    permission_required = ('is_superuser','is_staff',)

    group_permission = ""

    permission_denied_message = "L'utente non ha i Permessi Necessari"

    def dispatch(self, request, *args, **kwargs):
         '''

         :param request:
         :param args:
         :param kwargs:
         :return: controlliamo se gli utenti collegati sono staff o autenticati
         '''
         if not self.has_permission():
             messages.warning(self.request,self.permission_denied_message)
             return HttpResponseRedirect(reverse_lazy('base'))
         return super(AdminPermissionMixin,self).dispatch(request,args,kwargs)

    def has_permission(self):
         return super(AdminPermissionMixin,self).has_permission()

class LoginandPermissionMixin(PermissionRequiredMixin):

     permission_login_denied_message = 'Devi Prima Effettuare il Login'

     permission_denied_message = "L'utente non ha i Permessi Necessari"

     permission_required = ""


     def dispatch(self, request, *args, **kwargs):
         '''

         :param request:
         :param args:
         :param kwargs:
         :return: controlliamo se gli utenti collegati sono staff o autenticati
         '''

         if not self.request.user.is_authenticated():
             messages.warning(self.request,self.permission_login_denied_message)
             return redirect_to_login(next=self.request.path,login_url=self.get_login_url())
         if not self.has_permission():
             messages.warning(self.request,self.permission_denied_message)
             return HttpResponseRedirect(reverse_lazy('base'))
         return super(LoginandPermissionMixin,self).dispatch(request,args,kwargs)

     def has_permission(self):
         return super(LoginandPermissionMixin,self).has_permission()

# class getFilterUserMixin(object):
#
#     '''
#     Mixin per recuperare le liste degli utenti in base all'azineda di appartenenza
#     da utilizzare per ogni lista.
#     '''
#
#     def get_queryset(self):
#          if not self.request.user.is_superuser:
#             user_for_company = Company.objects.get(azienda_user__username=self.request.user.username)
#             user_for_azi = UserProfile.objects.filter(azienda__denominazione=user_for_company.denominazione).exclude(username=self.request.user.username)
#             return user_for_azi
#          return super(getFilterUserMixin,self).get_queryset()

class userList(LoginandPermissionMixin,getFilterUserMixin,ListView):

     '''
     Per visualizzare le list usiamo ListView di django supportato
     da LoginandPermissionMixin
     Per visualizzare la pagina degli utenti e quindi operare su ognuno di loro
     devi essere menbro dello staff
     se non fosse vieni rindirizzato alla pagina di dashboard con Errore
     '''

     model = UserProfile

     template_name = 'userManagement/page-user-list.html'

     permission_required = 'user.Can_View'

class userEdit(LoginandPermissionMixin,UpdateView):
    '''
    Per visualizzare le modifiche sugli utenti utilizzaimo update view
    supportata da permissionmixin.
    '''

    template_name = 'userManagement/page-user-edit.html'

    model = UserProfile

    permission_required = 'user.change_userprofile'

    form_class = UserFormEdit


    def get_success_url(self,**kwargs):

        messages.success(self.request,"L'utente %s è stato salvato con successo" % self.object.get_full_name())

        return reverse('utenti_lista')



    def form_valid(self, form):
        user_email_save = form.save(commit=False)
        user_email_save.email = form.cleaned_data['email']
        user_email_save.save()
        return super(userEdit,self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):


        if not self.request.user.is_superuser:
            user_for_company = Company.objects.filter(azienda_user__username=self.request.user.username)
            user_for_azi = UserProfile.objects.filter(azienda__denominazione=(c.denominazione for c in user_for_company))

            if not int(self.kwargs.get('pk')) in user_for_azi.values_list('pk',flat=True).order_by('pk'):
                messages.warning(self.request,self.permission_denied_message)
                return HttpResponseRedirect(reverse_lazy('base'))
        return super(userEdit,self).dispatch(request,args,kwargs)

class ProfileOnlyEdit(LoginRequiredMixin,UpdateView):

    '''
    Modifica solo alcuni campi dell'utente attualmete collegato
    l'utente per motivi di sicurezza puo solo modificare solo il suo
    profilo
    '''

    template_name = 'profileEdit/profile_edit.html'

    permission_required = 'user.change_userprofile'

    model = UserFormEdit.Meta.model

    form_class = profileEdit


    def check_user_profile_update(self,request):
        '''
        Ritorna vero se l'oggetto pk è uguale all oggetto richiesto tramite http (pk)
        :param request: request
        :return: Boolen True o false
        '''
        if request.user.is_authenticated():
           self.object = self.get_object()
           return self.object.pk == request.user.pk
        return False

    def dispatch(self, request, *args, **kwargs):
         '''
         Controlla se l'utente è abilitato a modificare.
         :param request:
         :param args:
         :param kwargs:
         :return:
         '''
         if not self.check_user_profile_update(request):
            messages.warning(self.request,"L'utente non ha i permessi necessari.")
            return HttpResponseRedirect(reverse_lazy('base'))
         return super(ProfileOnlyEdit,self).dispatch(request,args,kwargs)


    def form_valid(self, form):
        form.save()
        return super(ProfileOnlyEdit,self).form_valid(form)

    def get_success_url(self,**kwargs):
        messages.success(self.request,"L'utente %s è stato salvato con successo" % self.get_object())

        return reverse('utenti_lista')

class userDel(LoginandPermissionMixin,View):

    permission_required = ('user.delete_userprofile',)

    template_list_success = 'azienda/page-azienda-list.html'

    def get(self,request,*args,**kwargs):
        '''
        Cancella il gruppo
        '''
        user_client_delete = UserProfile.objects.get(username=self.request.GET.get('userdelete'))
        user_client_delete.delete()
        self.kwargs['success'] = "L'User è stato eliminato con successo"
        return JsonResponse(self.kwargs)

class userDelete(LoginandPermissionMixin,DeleteView):

      '''
      Cancella l'Utente selezionato se l'utente non estiste visualizza un warning
      (da modificare)
      '''
      template_name = 'userManagement/page-user-delete.html'

      model = UserProfile

      permission_required = 'user.delete_userprofile'

      def get_success_url(self,**kwargs):

        messages.success(self.request,"L'utente con id %s è stato eliminato con successo" % self.user_change_save.get_full_name())

        return reverse('utenti_lista')

class userCreate(LoginandPermissionMixin,CreateView):

      '''
      Crea un utente tramite Create View
      '''

      template_name = 'userManagement/page-user-create.html'

      form_class = UserFormAdd

      permission_required = 'user.add_userprofile'
      model = UserProfile

      def form_valid(self, form):

          self.save_new_user = form.save(commit=False)
          self.save_new_user.date_joined = datetime.datetime.now()
          self.save_new_user.save()
          for user_ in form.cleaned_data['user_permissions']:
              last_user = UserProfile.objects.last()
              last_user.user_permissions.add(user_.pk)
              last_user.save()

          return super(userCreate,self).form_valid(form)

      def get_success_url(self,**kwargs):

        messages.success(self.request,"L'utente %s è stato salvato con successo" % self.object)

        return reverse('utenti_lista')

class userChangePassword(LoginandPermissionMixin,SingleObjectMixin,FormView):
     '''
     Cambia la password degli utenti solo il superuser puo modificare
     '''
     template_name ='changePassword/page-change-password-user.html'

     form_class = ChangePasswordUser

     model = UserProfile

     permission_required = "user.Can_Password"

     def dispatch(self, request, *args, **kwargs):
         '''
         Richiama l'oggetto dal metofo get_objct che identifica l'utente collegato
         '''
         my_user = get_object_or_404(UserProfile ,pk=kwargs.get('pk'))
         self.object = self.get_object()
         return super(userChangePassword,self).dispatch(request,args,kwargs)

     def get_form_kwargs(self):
            self.user_pass = super(userChangePassword,self).get_form_kwargs()
            self.user_pass['user'] = self.object
            return self.user_pass

     def form_valid(self, form):
         '''
         Verifica che ilform sia valido e set la password
         '''
         self.object.set_password(form.cleaned_data['new_password1'])
         self.object.save()
         return super(userChangePassword,self).form_valid(form)

     def get_success_url(self,**kwargs):
        '''
        in caso di form corretto rindirizza alla pagina lista
        '''
        messages.success(self.request,"L'utente %s è stato salvato con successo" % self.get_object())

        return reverse('utenti_lista')

class ProfilePasswordChange(FormView):
      '''
      Classe per cambiare la classedell'utente collegato
      '''
      form_class = ChangePasswordUser
      template_name = 'changePassword/page-change-password-user.html'


      def form_valid(self, form):

          form.save()
          update_session_auth_hash(self.request)
          return super(ProfilePasswordChange,self).form_valid(form)


      def get_success_url(self,**kwargs):

        messages.success(self.request,"L'utente %s è stato salvato con successo" % 'ciao')

        return reverse('utenti_lista')

@login_required()
def Update(request):
    '''
    Modifica la password dell'utente collegato
    '''
    #da trasformane in class
    form = ChangePasswordUser(user=request.user)

    if request.method == 'POST':
        form = ChangePasswordUser(user=request.user,data=request.POST)
        if form.is_valid():
           form.save()
           update_session_auth_hash(request,form.user)
           messages.success(request,"L'utente %s è stato salvato con successo" % request.user)
           return HttpResponseRedirect(reverse('utenti_lista'))
    return render(request, 'changePassword/page-change-password-user.html',{'form':form})

@csrf_exempt
def api_get_check_user(request):

    try:
        client_save_ticket = ClientUserCompany.objects.get(pk=request.GET.get('cli_id'))
    except:
        return JsonResponse({'data':'Nessun Dato'})

    client_save_ticket.is_complete = True
    client_save_ticket.save()

    return JsonResponse(({'data':'Ok salvato'}))

@csrf_exempt
def api_get_uncheck_user(request):

    try:
        client_save_ticket = ClientUserCompany.objects.get(pk=request.GET.get('cli_id'))
    except:
        return JsonResponse({'data':'Nessun Dato'})

    client_save_ticket.is_complete = False
    client_save_ticket.save()

    return JsonResponse({'data':'Ok salvato'})

