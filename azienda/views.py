#Django
from django.core.urlresolvers import reverse_lazy,reverse

from django.views.generic import View,CreateView,UpdateView,DeleteView,ListView
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
#Base
from .forms import AziendaForm,AziendaEdit
from .models import Company
from client.models import ClientUserCompany
from user.models import UserProfile
from user.views import getFilterUserMixin,LoginandPermissionMixin

import json

#External


class getFilterCompanyMixin(object):

    '''
    Mixin per recuperare le liste della azienda in base all'utente loggato
    '''

    def get_queryset(self):

        if not self.request.user.is_superuser:
           user_for_company = Company.objects.filter(azienda_user__username=self.request.user.username)
           return user_for_company
        return super(getFilterCompanyMixin,self).get_queryset()

class aziendaAdd(LoginandPermissionMixin,CreateView):
    '''
    Crea l'azienda utilizziamo createviev , inserire i premessi solo
    al gruppo superuser
    '''

    permission_login_denied_message = 'Devi Prima Effettuare Il Login'

    permission_required = ('azienda.add_company')

    template_name = 'azienda/page-azienda-create.html'

    form_class = AziendaForm

    success_url = reverse_lazy('azienda_list')

    def form_valid(self, form):
        # se form valid rindirizza su template corretto
        form.save()

        return super(aziendaAdd,self).form_valid(form)


    def dispatch(self, request, *args, **kwargs):
         '''
         Il dispath è richiamato da loginrequiredmixin(bisogna essere autenticati per loggarsi)
         se l'Utente non è autenticato rindirizza su default get_login_url
         '''
         if not self.request.user.is_authenticated():
            messages.warning(self.request,self.permission_login_denied_message)
            return redirect_to_login(next=self.request.path,login_url=self.get_login_url())
         return super(aziendaAdd,self).dispatch(request,args,kwargs)

class aziendaUser(getFilterCompanyMixin,View):
    '''
    Chiamate Ajax
    '''

    def get(self, request, *args, **kwargs):
         utenti_azienda = list((user_.username,user_.pk) for user_ in UserProfile.objects.filter(azienda__denominazione=self.request.GET.get('usertotali')))
         self.kwargs[str(self.request.GET.get('usertotali'))] = utenti_azienda
         return JsonResponse(self.kwargs)

class aziendaCli(getFilterUserMixin,View):
    '''
    Chiamate Ajax
    '''
    def get(self, request, *args, **kwargs):
         clienti_azienda = list((user_.denominazione,user_.id) for user_ in ClientUserCompany.objects.filter(user__azienda__denominazione=self.request.GET.get('clitotali')))
         self.kwargs[str(self.request.GET.get('clitotali'))] = clienti_azienda
         return JsonResponse(self.kwargs)

class aziendaList(LoginandPermissionMixin,getFilterCompanyMixin,ListView):
    '''
    Lista di tutte le azienda viene inoltreinserto numero di dipendenti e numero clienti
    '''
    # viene visualizza solo da user della stessa azienda
    template_name = 'azienda/page-azienda-list.html'

    permission_login_denied_message = 'Devi Prima Effettuare Il Login'

    permission_required = ('azienda.Can_View',)

    model = Company

    def get_context_data(self, **kwargs):
        '''

        :param kwargs: null
        :return: ritorna il numero di utenti e numero di clienti per azienda
        '''
        self.kwargs_,self.kwargs__ = {},{}
        for control in Company.objects.all():
           numero_dipendenti_azienda = UserProfile.objects.filter(azienda__denominazione=control.denominazione).count()
           numero_clienti_azienda = ClientUserCompany.objects.filter(user__azienda__denominazione=control.denominazione).count()
           self.kwargs_[str(control.denominazione)] = numero_dipendenti_azienda
           self.kwargs__[str(control.denominazione)] = numero_clienti_azienda
        numero_utenti = super(aziendaList,self).get_context_data(**kwargs)
        numero_utenti['number'] = self.kwargs_
        numero_utenti['number_cli'] = self.kwargs__
        return numero_utenti

class aziendaDelete(LoginandPermissionMixin,DeleteView):
    '''
    Cancella singola azienda
    '''
    # da inserire solo superuser
    model = Company
    template_name = 'azienda/page-azienda-delete.html'

    permission_required = ('azienda.delete_company',)

    permission_login_denied_message = 'Devi Prima Effettuare Il Login'

    def get_success_url(self,**kwargs):
       '''
       Se viene cancellata l'azineda scelta viene rindirizzato a azineda list
       '''
       messages.warning(self.request,"L'azienda %s è stata eliminata con successo" % self.object.denominazione)

       return reverse('azienda_list')

    def get_context_data(self, **kwargs):
         '''
         Invia utenti e clienti che fanno parte dell'azienda che si vuole eliminare
         '''
         self.user_connect_to_azienda = super(aziendaDelete,self).get_context_data()
         self.user_connect_to_azienda['user_azienda'] = UserProfile.objects.filter(azienda__denominazione=self.object)
         self.user_connect_to_azienda['client_azienda'] = ClientUserCompany.objects.filter(user__azienda__denominazione=self.object)
         return self.user_connect_to_azienda


class aziendaDel(LoginandPermissionMixin,View):

    permission_required = ('azienda.delete_company',)

    permission_login_denied_message = 'Devi Prima Effettuare Il Login'

    template_list_success = 'azienda/page-azienda-list.html'

    def get(self,request,*args,**kwargs):
        self.request.GET.get('userdelete')
        user_client_delete = Company.objects.get(denominazione=self.request.GET.get('userdelete'))
        user_client_delete.delete()
        self.kwargs['success'] = "L'Azienda è stata eliminata con successo"
        return JsonResponse(self.kwargs)


class aziendaEdit(LoginandPermissionMixin,UpdateView):

    template_name = 'azienda/page-azienda-edit.html'

    model = Company

    permission_required = ('azienda.change_company')

    permission_login_denied_message = 'Devi Prima Effettuare Il Login'

    form_class = AziendaEdit

    def form_valid(self, form):
        '''
        Salva il form se tutto è corretto prendendo il cf
        '''
        form_all = form.save(commit=False)
        form_all.cf = form.cleaned_data['cf']
        form_all.save()
        return super(aziendaEdit,self).form_valid(form)

    def get_success_url(self,**kwargs):
       '''
       Se viene modifica l 'azienda rindirizza su azienda_list
       '''

       messages.warning(self.request,"L'azienda %s è stata salvata con successo" % self.object.denominazione)

       return reverse('azienda_list')


    def dispatch(self, request, *args, **kwargs):
        '''
        Aggiunge a dispatch del LoginandPermissionRequiredMixin altro controllo,
        se l'utente dovesse avere i permessi di modifca, non puo avere i permessi per
        modificare altri user che non siano della stessa azienda.
        '''
        user_for_company = Company.objects.filter(azienda_user__username=self.request.user.username)
        if not self.request.user.is_superuser:
            if not int(self.kwargs.get('pk')) in user_for_company.values_list('pk',flat=True).order_by('pk'):
                messages.warning(self.request,self.permission_denied_message)
                return HttpResponseRedirect(reverse_lazy('base'))
        return super(aziendaEdit,self).dispatch(request,args,kwargs)