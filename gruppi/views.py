#Django
from django.contrib import messages
from django.shortcuts import reverse
from django.views.generic import View,CreateView,ListView,UpdateView,DeleteView
from django.contrib.auth.models import Group
from django.http import JsonResponse

#Base
from user.views import LoginandPermissionMixin
from user.models import UserProfile
from .forms import formGroups

class groupsAdd(LoginandPermissionMixin,CreateView):
      '''
      Crea i gruppi con i permessi

      '''
      permission_required = ('auth.add_group',)

      form_class = formGroups

      template_name = 'groups/page-groups-create.html'

      def form_valid(self, form):
          form.save()
          return super(groupsAdd,self).form_valid(form)

      def get_success_url(self,**kwargs):

        messages.success(self.request,"Il Gruppo %s è stato salvato con successo" % self.object )

        return reverse('gruppi_lista')


class groupsList(LoginandPermissionMixin,ListView):
      '''
      Lista di tutti i gruppi e relativi permessi
      '''


      permission_required = ("auth.Can_View")

      template_name = 'groups/page-groups-list.html'

      model =  Group

      def dispatch(self, request, *args, **kwargs):
          return super(groupsList,self).dispatch(request,args,kwargs)

      def has_permission(self):
          return super(groupsList,self).has_permission()


class groupEdit(LoginandPermissionMixin,UpdateView):

     '''
     Modifca il Gruppo con relativi permessi.

     '''

     template_name = 'groups/page-groups-edit.html'

     model = Group

     form_class = formGroups

     def get_success_url(self,**kwargs):

         messages.success(self.request,"Il Gruppo %s è stato salvato con successo" % self.object)

         return reverse('gruppi_lista')


     def form_valid(self, form):
          form.save()
          return super(groupEdit,self).form_valid(form)

class groupDelete(LoginandPermissionMixin,DeleteView):


      template_name = 'groups/page-groups-delete.html'

      model = Group

      permission_required = 'auth.delete_group'

      def get_context_data(self, **kwargs):
         self.user_conect_to_groups = super(groupDelete,self).get_context_data()
         self.user_conect_to_groups['user_groups'] = UserProfile.objects.filter(groups=self.object)
         return self.user_conect_to_groups

      def get_success_url(self,**kwargs):

        messages.warning(self.request,"Il gruppo è stato eliminato con successo" % self.object.denominazione)   #self.user_change_save.get_full_name())

        return reverse('gruppi_lista')

class groupDel(LoginandPermissionMixin,View):

    permission_required = ('auth.delete_group',)

    template_list_success = 'azienda/page-azienda-list.html'



    def get(self,request,*args,**kwargs):
        '''
        Cancella il gruppo
        '''
        user_client_delete = Group.objects.get(name=self.request.GET.get('userdelete'))
        user_client_delete.delete()
        self.kwargs['success'] = "Il Gruppo è stato eliminato con successo"
        return JsonResponse(self.kwargs)