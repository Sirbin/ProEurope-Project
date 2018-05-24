#Django
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url,handler404,handler500
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from user.forms import FormLogin,FormPassChange,SetPassword
import user.views

#Base
from user.views import userList,userEdit,userDelete,userCreate,ProfileOnlyEdit,userChangePassword,DashboardUser,userDel,api_get_check_user, api_get_uncheck_user

from client.views import clientCreate,clientList,clientDelete,clientAttach,clientDel,clientUpdate,zipAllattch
from azienda.views import aziendaAdd,aziendaList,aziendaDelete,aziendaUser,aziendaEdit,aziendaCli,aziendaDel
from gruppi.views import groupsAdd,groupsList,groupDelete,groupEdit,groupDel
from registrationuSER.views import confermRegistrationDoneok,registration,completeRegistrazione
from modulistica.views import addforms, getNameModul
#static
from django.conf.urls.static import static



urlpatterns = [



    #Admin
    url(r'^admin/', admin.site.urls),

    #Procedure di Autenticazione e Reset Password
    url(r'^login/$', views.login,{'template_name':'login/page-login.html','authentication_form': FormLogin } ,name='login'),
    url(r'^logout/$',login_required(views.logout),{'template_name':'logout/logout.html','extra_context':{'Saluti':'Hai chiuso la sessione'}},name='logout'),
    url(r'^password/reset/$',views.password_reset,{'template_name':'recoveryPass/page-recoverpw.html','password_reset_form':FormPassChange,'post_reset_redirect':reverse_lazy('send'),
                                                   'email_template_name':'recoveryPass/page-reset-email.html'},name='passreset'),
    url(r'^password/reset/send/$',views.password_reset_done,{'template_name':'recoveryPass/page-confirm-mail.html',
                                                             'extra_context':{'current_site':settings.SITE_NAME}},name='send'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$',views.password_reset_confirm,{'post_reset_redirect':reverse_lazy('pw_done'),
                                                                                                  'set_password_form':SetPassword,
                                                                                                  'template_name':'recoveryPass/page-confirm-pw.html'},name='password_reset_confirm'),
    url(r'^password/reset/done/$',views.password_reset_done,{'template_name':'recoveryPass/page-confirm-pw-done.html'},name='pw_done'),
    #Registrazione
    url(r'^registrazione/$',registration.as_view(),name='registrazione'),
    url(r'^registrazione/done/$',confermRegistrationDoneok.as_view(),name='registrazione_done'),
    url(r'^registrazione/complete/$',completeRegistrazione.as_view(),name='registrazione_complete'),

    #Base
    #url(r'^$', user.views.dashboard, name='base'),
    url(r'^$',DashboardUser.as_view(),name='base'),

    #Azienda
    url(r'^azienda/lista/$',aziendaList.as_view(),name='azienda_list'),
    url(r'^azienda/create/$',aziendaAdd.as_view(),name='azienda_add'),
    url(r'^azienda/delete/(?P<pk>\d+)/$',aziendaDelete.as_view(),name='azienda_delete'),
    url(r'^azienda/edit/(?P<pk>\d+)/$',aziendaEdit.as_view(),name='azienda_edit'),

    #Call Ajax
    url(r'^azienda/user/$',aziendaUser.as_view(),name='azienda_ajax'),
    url(r'^azienda/cli/$',aziendaCli.as_view(),name='azienda_cli_ajax'),
    url(r'^azienda/user/delete/$',aziendaDel.as_view(),name='azienda_del_ajax'),
    url(r'^api/check/$',api_get_check_user,name="check_complete"),
    url(r'^api/uncheck/$',api_get_uncheck_user,name="uncheck_complete"),


    #Utenti
    url(r'^utenti/lista/$',userList.as_view(),name='utenti_lista'),
    url(r'^utenti/edit/(?P<pk>\d+)/$',userEdit.as_view(),name='utenti_edit'),
    url(r'^utenti/delete/(?P<pk>\d+)/$',userDelete.as_view(),name='utenti_delete'),
    url(r'^utenti/create/$',userCreate.as_view(),name='utenti_add'),
    url(r'^utenti/password-change/(?P<pk>\d+)/$',userChangePassword.as_view(),name='profile_password_change_for_id'),
    #Call Ajax User
    url(r'^utenti/user/delete/$',userDel.as_view(),name='user_del_ajax'),

    #Profili
    url(r'^profile/(?P<pk>\d+)/$',ProfileOnlyEdit.as_view(),name='profile_edit'),
    url(r'^profile/password-change/$',user.views.Update,name='profile_password_change'),

    #Gruppi
    url(r'^gruppi/lista/$',groupsList.as_view(),name='gruppi_lista'),
    url(r'^gruppi/create/$',groupsAdd.as_view(),name='gruppi_add'),
    url(r'^gruppi/delete/(?P<pk>\d+)/$',groupDelete.as_view(),name='gruppi_delete'),
    url(r'^gruppi/edit/(?P<pk>\d+)/$',groupEdit.as_view(),name='gruppi_edit'),

    #Call Ajax Groups
    url(r'^gruppi/user/delete/$',groupDel.as_view(),name='gruppi_del_ajax'),

    #Clienti
    url(r'^client/create/$',clientCreate.as_view(),name='clienti_add'),
    url(r'^client/lista/$',clientList.as_view(),name='clienti_lista'),
    url(r'^client/delete/(?P<pk>\d+)/$',clientDelete.as_view(),name='clienti_delete'),
    url(r'^client/edit/(?P<pk>\d+)/$',clientUpdate.as_view(),name='clienti_edit'),

    #Call Ajax Client
    url(r'^client/user/delete/$',clientDel.as_view(),name='client_del_ajax'),

    #Client Attachments
    url(r'^client/attachments/(?P<pk>\d+)/$',clientAttach.as_view(),name='clienti_attach'),
    url(r'^client/attachments/(?P<pk>\d+)/all/$',zipAllattch.as_view(),name='clienti_attach_all'),

    #Modulistica
    url(r'^modulistica/create/$',addforms.as_view(),name='modulistica'),
    url(r'^modulistica/create/(?P<filename>.*)/$',getNameModul.as_view(),name='get'),

]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


handler404 = 'ProEurope.views.page_not_found'

handler500 = 'ProEurope.views.page_error'