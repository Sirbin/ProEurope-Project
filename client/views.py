#Django
from django.core.urlresolvers import reverse_lazy,reverse
from django.shortcuts import render,HttpResponse,HttpResponseRedirect, redirect
from django.conf import settings
from django.views.generic import TemplateView,View,CreateView,UpdateView,DeleteView,ListView,DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.http import JsonResponse
#Base
from .forms import clientForm, attachedClientForm
from .models import ClientUserCompany,CreateFolderUser
from user.views import LoginandPermissionMixin
from user.models import UserProfile
from azienda.models import Company
#External
import os

class clientAttached(LoginandPermissionMixin,FormView):

      template_name = 'client/page-client-attachments-new.html'

      permission_required = ('client.add_clientusercompany',)

      form_class = attachedClientForm

      f = CreateFolderUser()

      def dispatch(self, request, *args, **kwargs):

          self.get_denominazione = ClientUserCompany.objects.get(pk=self.kwargs.get('pk'))

          return super(clientAttached,self).dispatch(request,args,kwargs)

      def form_valid(self, form):

          if not self.f.exists_file(str(self.get_denominazione)):
              f = CreateFolderUser()
              f.create_folder(name=str(self.get_denominazione))
          nome_file = self.request.POST.get('nome_allegato',"")
          CreateFolderUser.save_file_denominazione(self.request.FILES['allegato'],nome_file,CreateFolderUser.path_create, str(self.get_denominazione))

          return super(clientAttached, self).form_valid(form)

      def get_context_data(self, **kwargs):
          '''
              Recupera i file al'interno della cartella del Cliente
          '''

          try:
            analytics_list = os.listdir(os.path.join(CreateFolderUser.path_create,str(self.get_denominazione)))
          except:
              analytics_list = []

          c = super(clientAttached, self).get_context_data(**kwargs)
          c['allegato'] = analytics_list
          c['id'] = self.kwargs.get('pk')
          c['set'] = settings.MEDIA_ROOT
          c['user'] = self.get_denominazione

          return c

      def get_success_url(self, **kwargs):

          messages.success(self.request, "Allegati Salvati con successo")

          return reverse('client_attach_new', kwargs={'pk':self.kwargs.get('pk')})

class getNameAttach(LoginandPermissionMixin,View):
    '''
     Scarica l'allegato corrispondente 
    '''

    permission_required = ('client.add_clientusercompany',)

    def dispatch(self, request, *args, **kwargs):
        self.getPdf = kwargs['filename']

        self.get_denominazione = ClientUserCompany.objects.get(pk=self.kwargs.get('pk'))

        return super(getNameAttach,self).dispatch(request, args, kwargs)

    def get(self,request,*args,**kwargs):


        f = CreateFolderUser.path_create
        getPdfFile = open(os.path.join(os.path.join(f, str(self.get_denominazione)), self.getPdf),'rb')
        response = HttpResponse(getPdfFile.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % self.getPdf
        getPdfFile.close()
        return response

class delNameAttach(View):
    '''
        Cancella gli Allegati     
    '''

    # permission_required = ('client.delete_clientusercompany',)

    template_name = 'client/page-client-attachment-client-delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.getPdf = kwargs['filename']

        self.get_denominazione = ClientUserCompany.objects.get(pk=self.kwargs.get('pk'))

        return super(delNameAttach, self).dispatch(request, args, kwargs)

    def get(self, request, *args, **kwargs):

        context_path = {
            'file': self.getPdf,
            'id': self.kwargs.get('pk')
        }
        f = CreateFolderUser.path_create
        try:
            os.remove((os.path.join(os.path.join(f, str(self.get_denominazione)), self.getPdf)))
        except:
            error_messages = 'Impossibile eliminare il file'
            context_path['error'] = error_messages

        return render(request, template_name=self.template_name, context=context_path)

class clientCreate(LoginandPermissionMixin,CreateView,SingleObjectMixin):


    template_name = 'client/page-client-create.html'

    permission_required = ('client.add_clientusercompany',)

    model = ClientUserCompany


    form_class = clientForm

    def get_list(self,list):
        return list[0]

    def get_form_kwargs(self):
        '''
        Tramite get_form_kwarg invio all init del form l'utente che è collegato
        cosi da visualizzare le aziende che sono collegate a l'utente.
        '''

        try:
            self.mio_groups = self.get_list([c for c in self.request.user.groups.values_list('name',flat=True)])
        except:
            self.mio_groups = None

        kwargs = super(clientCreate, self).get_form_kwargs()
        kwargs['username'] = self.request.user.username
        kwargs['group'] = self.mio_groups
        print('ciao')
        return kwargs



    def form_valid(self, form):

        f = CreateFolderUser()
        f.create_folder(name=form.cleaned_data['denominazione'])

        return super(clientCreate,self).form_valid(form)

    def get_success_url(self,**kwargs):

        self.mypk = self.get_form_kwargs().get('instance')

        messages.success(self.request,"L'utente è stato salvato con successo" )

        return reverse('client_attach_new', kwargs={'pk':self.mypk.pk})

class clientUpdate(LoginandPermissionMixin,UpdateView,CreateFolderUser):


    template_name = 'client/page-client-edit.html'

    permission_required = ('client.change_clientusercompany',)

    model = ClientUserCompany

    form_class = clientForm

    # evetualmente da eliminare subito in caso di errore
    def form_valid(self, form):
        get_all_file_to_altri_allegati = self.request.FILES.getlist('altri_allegati')#

        if get_all_file_to_altri_allegati:
            f = CreateFolderUser()
            form_all = form.save(commit=False)

            f.create_zip_file_altri_allegati(get_all_file_to_altri_allegati, self.get_denominazione.denominazione)
            get_zip = f.get_file_zip(self.get_denominazione.denominazione)
            #form_all.allegati_autocertificazione = form.cleaned_data['allegati_autocertificazione']
            form_all.altri_allegati = get_zip
            form_all.save()

        return super(clientUpdate,self).form_valid(form)

    def get_list(self,list):
        return list[0]

    def get_context_data(self, **kwargs):

        c = super(clientUpdate,self).get_context_data(**kwargs)
        c['id'] = self.kwargs.get('pk')
        c['user'] = self.get_denominazione

        return c

    def dispatch(self, request, *args, **kwargs):
        self.get_denominazione = ClientUserCompany.objects.get(pk=self.kwargs.get('pk'))

        #user_for_company = Company.objects.filter(azienda_user__username=self.request.user.username)
        #user_for_azi = UserProfile.objects.filter(azienda__denominazione=(c.denominazione for c in user_for_company))
        if not self.request.user.is_superuser:
            user_for_company = Company.objects.filter(azienda_user__username=self.request.user.username)
            user_for_azi = UserProfile.objects.filter(azienda__denominazione=(c.denominazione for c in user_for_company))
            #if not int(self.kwargs.get('pk')) in user_for_azi.values_list('pk',flat=True).order_by('pk'):
            #    messages.warning(self.request,self.permission_denied_message)
            #    return HttpResponseRedirect(reverse_lazy('base'))
        return super(clientUpdate,self).dispatch(request,args,kwargs)

    def get_form_kwargs(self):
        '''
        Tramite get_form_kwarg invio all init del form l'utente che è collegato
        cosi da visualizzare le aziende che sono collegate a l'utente.
        '''
        try:
            self.mio_groups = self.get_list([c for c in self.request.user.groups.values_list('name',flat=True)]) #aggiunto 06/01
        except:
            self.mio_groups = None

        kwargs = super(clientUpdate, self).get_form_kwargs()
        kwargs['username'] = self.request.user.username
        kwargs['group'] = self.mio_groups

        return kwargs

    def get_success_url(self,**kwargs):

        messages.success(self.request,"L'utente %s è stato salvato con successo" % self.object)

        return reverse('clienti_lista')

class getFilterUserComanyMixin(object):

    '''
    Mixin per recuperare le liste degli utenti in base all'azineda di appartenenza
    da utilizzare per ogni lista.
    '''

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
         return super(getFilterUserComanyMixin,self).get_queryset()

class clientList(LoginandPermissionMixin,getFilterUserComanyMixin,ListView):
    '''
    List View ch visualizza tutti i clienti
    '''
    template_name = 'client/page-client-list.html'

    model = ClientUserCompany

    permission_required = ('client.Can_View')

    def get_context_data(self, **kwargs):
        '''
        Ritorna il numero di allegati che sono presenti per signolo utente
        '''
        clienti_user = super(clientList,self).get_context_data(**kwargs)
        for azienda_denominazione in ClientUserCompany.objects.all():
            self.cli2 = ClientUserCompany.objects.values('doc','cf_doc','attrribuzione_pi','certificato_camerale','visura_camerale',\
            'contratto','preventivi','mod_unico_anno_prec','mod_unico_anno_prec_2',\
            'bilancio_ultimi_2','bilancio_anno_corso','attestati','allegati_autocertificazione','altri_allegati').get(denominazione= azienda_denominazione.denominazione)
            kwargs[azienda_denominazione.denominazione] = list(j for j in self.cli2 if self.cli2.get(j)).__len__()
        clienti_user['numero_allegati'] = kwargs
        return clienti_user

class clientDetail(DetailView,CreateFolderUser):

    template_name = 'client/page-client-attachment-client-delete.html'

    model = ClientUserCompany

class clientAttach(LoginandPermissionMixin,ListView,CreateFolderUser):
    '''
    List View che visualizza tutti gli allegati per signolo utente
    '''
    template_name = 'client/page-client-attachment-client-list.html'

    permission_required = ('client.Can_View_att',)

    model = ClientUserCompany

    def get_queryset(self):
          '''Ritorna tutti gli allegati per signolo utente'''

          gt = ClientUserCompany.objects.filter(pk=self.kwargs.get('pk'))
          return gt #super(clientAttach,self).get_queryset()

    def dispatch(self, request, *args, **kwargs):
        '''
        Aggiunge controlli su permessi se l'utente ha il permesso di visualizzare gli allegati
        '''
        if not self.request.user.is_superuser:
             user_for_company = Company.objects.get(azienda_user__username=self.request.user.username)
             user_for_azi = ClientUserCompany.objects.filter(user__azienda__denominazione=user_for_company.denominazione)
             if not int(self.kwargs.get('pk')) in user_for_azi.values_list('pk',flat=True).order_by('pk'):
                messages.warning(self.request,self.permission_denied_message)
                return HttpResponseRedirect(reverse_lazy('base'))
        return super(clientAttach,self).dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):

            '''
            Ritorna Tutti data e ora degli accessi al file
            '''
            fs = CreateFolderUser()
            time_attachments = super(clientAttach,self).get_context_data(**kwargs)
            file_time = ClientUserCompany.objects.filter(pk=self.kwargs.get('pk'))
            for j in file_time:

                kwargs[j.doc.name] = fs.created_time(j.doc.name).strftime('%d-%m-%Y %H:%m')
                kwargs[j.cf_doc.name] = fs.accessed_time(j.cf_doc.name).strftime('%d-%m-%Y %H:%m')
                kwargs[j.attrribuzione_pi.name] = fs.accessed_time(j.attrribuzione_pi.name).strftime('%d-%m-%Y %H:%m')
                kwargs[j.certificato_camerale.name] = fs.accessed_time(j.certificato_camerale.name).strftime('%d-%m-%Y %H:%m')
                kwargs[j.visura_camerale.name] = fs.accessed_time(j.visura_camerale.name).strftime('%d-%m-%Y %H:%m')
                kwargs[j.contratto.name] = fs.accessed_time(j.contratto.name).strftime('%d-%m-%Y %H:%m')
                kwargs[j.preventivi.name] = fs.accessed_time(j.preventivi.name).strftime('%d-%m-%Y %H:%m')
                kwargs[j.mod_unico_anno_prec.name] = fs.accessed_time(j.mod_unico_anno_prec.name).strftime('%d-%m-%Y %H:%m')
                kwargs[j.mod_unico_anno_prec_2.name] = fs.accessed_time(j.mod_unico_anno_prec_2.name).strftime('%d-%m-%Y %H:%m')
                kwargs[j.bilancio_ultimi_2.name] = fs.accessed_time(j.bilancio_ultimi_2.name).strftime('%d-%m-%Y %H:%m')
                kwargs[j.bilancio_anno_corso.name] = fs.accessed_time(j.bilancio_anno_corso.name).strftime('%d-%m-%Y %H:%m')
                kwargs[j.attestati.name] = fs.accessed_time(j.attestati.name).strftime('%d-%m-%Y %H:%m')
                kwargs[j.allegati_autocertificazione.name] = fs.accessed_time(j.allegati_autocertificazione.name).strftime('%d-%m-%Y %H:%m')
                kwargs[j.altri_allegati.name] = fs.accessed_time(j.altri_allegati.name).strftime('%d-%m-%Y %H:%m')
            time_attachments['time'] = kwargs
            return time_attachments

class clientAttachDelete(DeleteView):

    '''da riprendere'''

    template_name = 'client/page-client-attachment-client-delete.html'

    def get_queryset(self):
        self.prova_file = ClientUserCompany.objects.filter(pk=self.kwargs.get('pk'))
        return self.prova_file

    def dispatch(self, request, *args, **kwargs):
        self.get_nome_file = self.kwargs['nome']
        self.sentenza = ClientUserCompany.objects.filter(pk=self.kwargs.get('pk'))
        self.sentenza_applello = self.sentenza.values('attrribuzione_pi','cf_doc').exists()
        return super(clientAttachDelete,self).dispatch(request,args,kwargs)

    def delete(self, request, *args, **kwargs):
        filename = CreateFolderUser()
        filename.delete(self.kwargs.get('nome'))
        return HttpResponseRedirect(reverse('clienti_lista'))

    def get_context_data(self, **kwargs):
        invio = super(clientAttachDelete,self).get_context_data(**kwargs)
        invio['nome'] = self.get_nome_file
        return invio

    def get_success_url(self,**kwargs):


       return reverse('clienti_lista')

class clientDel(LoginandPermissionMixin,View,CreateFolderUser):

    permission_required = ('client.delete_clientusercompany',)

    template_list_success = 'azienda/page-azienda-list.html'

    file =CreateFolderUser()

    def get(self,request,*args,**kwargs):
        '''
        Cancella client e tutti i file associati as esso
        '''
        user_client_delete = ClientUserCompany.objects.get(denominazione=self.request.GET.get('userdelete'))
        if self.file.exists_file(user_client_delete.denominazione):
             self.file.cancella_file(user_client_delete.denominazione)
        user_client_delete.delete()
        self.kwargs['success'] = "Il Cliente è stato eliminato con successo"
        return JsonResponse(self.kwargs)

class clientDelete(LoginandPermissionMixin,DeleteView,CreateFolderUser):
    '''
    Cancella singolo cliente
    '''
    model = ClientUserCompany

    file = CreateFolderUser()

    permission_required = ('client.delete_clientusercompany',)

    template_name = 'client/page-client-delete.html'

    def delete(self, request, *args, **kwargs):
        clientDeleteAllFile = ClientUserCompany.objects.get(pk=self.kwargs.get('pk'))
        if self.file.exists_file(clientDeleteAllFile.denominazione):
            self.file.cancella_file(clientDeleteAllFile.denominazione)
        return super(clientDelete,self).delete(request,args,kwargs)

    def get_success_url(self,**kwargs):

       messages.success(self.request,"Il cliente %s è stato eliminata con successo" % self.object )

       return reverse('clienti_lista')


class zipAllattch(LoginandPermissionMixin,TemplateView,CreateFolderUser):

    permission_required = ('client.Can_Down')

    error_attachment = 'Devi prima inserire degli allegati'

    def dispatch(self, request, *args, **kwargs):
         #self.clientDelete = ClientUserCompany.objects.get(pk=self.kwargs.get('pk'))
         return super(zipAllattch,self).dispatch(request,args,kwargs)

    def conteggio_allegati(self):
        self.clientDelete_ = ClientUserCompany.objects.values_list('doc','cf_doc','attrribuzione_pi','certificato_camerale','visura_camerale',\
                'contratto','preventivi','mod_unico_anno_prec','mod_unico_anno_prec_2',\
                'bilancio_ultimi_2','bilancio_anno_corso','attestati','allegati_autocertificazione','altri_allegati').get(pk=self.kwargs.get('pk'))
        numero_allegati = 0
        for j in self.clientDelete_:
            if j !="":
                numero_allegati +=1
        return int(numero_allegati)

    def get(self,request,*args,**kwargs):
        self.clientDelete = ClientUserCompany.objects.get(pk=self.kwargs.get('pk'))
        if self.conteggio_allegati() != 0:
            f = CreateFolderUser()
            f.create_zip_file(self.clientDelete.denominazione)
            zip_file = open(os.path.join(os.path.dirname(settings.BASE_DIR),'ProEurope-Project','static','media',self.clientDelete.denominazione+'.zip'), 'rb')#,encoding='ISO-8859-1')
            response = HttpResponse(zip_file,content_type='application/zip')#'application/force-download')
            #(zip_file, content_type='application/force-download')
            #response['id'] = self.clientDelete.id
            response['Content-Disposition'] = 'attachment; filename="%s"' % zip_file.name
            return response
        messages.warning(self.request,self.error_attachment)
        return HttpResponseRedirect(reverse_lazy('base'))

