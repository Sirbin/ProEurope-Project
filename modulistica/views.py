from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy,reverse
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.views.generic import TemplateView,View,CreateView,UpdateView,DeleteView,ListView,DetailView,FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.http import JsonResponse
from client.models import CreateFolderUser
#Base
from client.forms import clientForm
from  .forms import UploadFileForm

from user.views import LoginandPermissionMixin
from user.models import UserProfile
from azienda.models import Company
#External
import os

# Create your views here.


class addforms(LoginandPermissionMixin, FormView):



    template_name = 'formsProEurope/page-forms-attachment.html'

    form_class = UploadFileForm


    permission_required = ('client.add_clientusercompany',)


    def get_context_data(self, **kwargs):
        '''
            Recupera i file al'interno della cartella Modulistica
        '''


        analytics_list = os.listdir(CreateFolderUser.path_create_form)
        c = super(addforms, self).get_context_data(**kwargs)
        c['modulistica'] = analytics_list
        c['set'] = settings.FORM_ROOT

        return c

    def form_valid(self, form):


        CreateFolderUser.save_file(self.request.FILES['modulistica'],CreateFolderUser.path_create_form)

        #form.save()
        #update_session_auth_hash(self.request)
        return super(addforms, self).form_valid(form)


    def form_invalid(self, form):
        print(self.request.FILES)
        return super(addforms, self).form_invalid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, "Modulistica Salvata con successo")

        return reverse('modulistica')


class getNameModul(LoginandPermissionMixin,View):
    '''
     Scarica il File Pdf corrispondente
    '''

    permission_required = ('client.add_clientusercompany',)

    def dispatch(self, request, *args, **kwargs):
        self.getPdf = kwargs['filename']

        return super(getNameModul,self).dispatch(request, args, kwargs)

    def get(self,request,*args,**kwargs):


        f = CreateFolderUser.path_create_form
        getPdfFile = open(os.path.join(f, self.getPdf),'rb')
        response = HttpResponse(getPdfFile.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % self.getPdf
        getPdfFile.close()
        return response


class delNameModul(View):
    '''
        Cancella i moduli in base al nome    
    '''
    file = CreateFolderUser()

    #permission_required = ('client.delete_clientusercompany',)

    template_name = 'formsProEurope/page-forms-delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.getPdf = kwargs['filename']

        return super(delNameModul, self).dispatch(request, args, kwargs)

    def get(self,request,*args,**kwargs):

        context_path = {
            'file': self.getPdf
        }
        f = CreateFolderUser.path_create_form
        try:
            os.remove((os.path.join(f, self.getPdf)))
        except:
            error_messages = 'Impossibile eliminare il file'
            context_path['error'] = error_messages

        return render(request,template_name=self.template_name, context=context_path)

