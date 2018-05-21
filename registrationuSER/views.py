from user.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render
from django.core.mail import mail_admins,send_mail,mail_managers
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView,FormView,RedirectView
from django.contrib import messages
from django.template.loader import render_to_string
from .forms import FormRegistrationMixin

class registration(FormView):

    ''' Tramite il formView di django
     prendiamo il template di riferimento template_name
     il fomr di riferimento form_class
     tramite il get invieremo al template ilform_class,
     quando il nuovo utente verrà registrato sara rindirizzato al template corretto di avvenuta registrazione.
     cliccando sulla url verra rindirizzaro all'interno dell'applicazione per completare la registrazione.
     l'utente è ancora disable.
    '''

    template_name = 'register/page-registration.html'
    form_class = FormRegistrationMixin
    success_url = reverse_lazy('registrazione_done')

    get_username = ""

    def get(self, request, *args, **kwargs):

         '''Invio il form al template'''

         form = FormRegistrationMixin
         content = {'form':form}
         return render(request,template_name=self.template_name,context=content)

    def form_valid(self, form):

        '''
        Se il form è validato(vedi form di riferimento),
        salverà l'utente.
        :param form:
        :return:
        '''
        user_register_ = form.save(commit=False)
        user_register_.is_active = False
        user_register_.is_staff = False
        user_register_.save()
        utenteRegistrato = UserProfile.objects.get_by_natural_key(username=form.cleaned_data['username'])
        msg_html = render_to_string('register/email_send_admin.html',{'username':utenteRegistrato,'username_id':utenteRegistrato.id,'domain':get_current_site(self.request)})
        mail_managers(subject='Email per Amministratori',message="",html_message=msg_html)
        #send_mail(subject='Email per Amministratori',message="",from_email='Amministatore@',['alessiobino@hotmail.it'],html_message=msg_html)
        return super(registration,self).form_valid(form)




    def get_success_url(self):
         '''
         In caso di successo del form verrà indirizzaro al seguente url
         :return: 'registrazione_done
         '''
         return reverse_lazy('registrazione_done')

class confermRegistrationDoneok(TemplateView):

    template_name = 'register/page-registration-done.html'

    def dispatch(self, request, *args, **kwargs):
        return super(confermRegistrationDoneok,self).dispatch(request,*args,**kwargs)

class completeRegistrazione(LoginRequiredMixin,RedirectView):
     '''
     Ad essere sicero non so perche è stata implementata nel caso sia completo rindirizza al utente in vase al suo id/pk
     '''
     permanent = True

     pattern_name = 'utenti_edit'

     permission_login_denied_message = 'Devi Prima Effettuare Il Login'

     def get_redirect_url(self, *args, **kwargs):
         '''
         Rindirizza al l'utente id
         '''

         return reverse_lazy('utenti_edit',args=(self.kwargs['pk'],))

     def dispatch(self, request, *args, **kwargs):
         '''
         Il dispath è richiamato da loginrequiredmixin(bisogna essere autenticati per loggarsi)
         se l'Utente non è autenticato rindirizza su default get_login_url
         '''
         if not self.request.user.is_authenticated():
            messages.warning(self.request,self.permission_login_denied_message)
            return redirect_to_login(next=self.request.path,login_url=self.get_login_url())
         return super(completeRegistrazione,self).dispatch(request,args,kwargs)