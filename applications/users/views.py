from django.shortcuts import render
#para el email
from django.core.mail import send_mail
#para las urls
from django.urls import reverse_lazy, reverse
#para logear a los usuarios
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


from django.views.generic import (
    View,
    CreateView
)

from django.views.generic.edit import (
    FormView
)
#Mi codigo
from .models import User
from .functions import code_generator
from secret import get_secret
from .forms import (
    UserRegisterForm, 
    LoginForm, 
    UpdateFormPass,
    Verification
)

class UserRegisterCreateView(FormView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = '/'

    def form_valid(self, form):
        #generar codigo para activar usuario
        code = code_generator()
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            first_name = form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name'],
            geneder = form.cleaned_data['geneder'],
            code_register = code,
        )
        #enviar el codigo por e-mail
        asunto = 'Confimacion de e-mail'
        mensaje = 'Codego de verificación: ' + code
        email_remi = get_secret("E-MAIL")
        send_mail(asunto, mensaje,email_remi, [form.cleaned_data['email']])
        #redirigir a pantalla de verificacion
        return HttpResponseRedirect(
            reverse(
                'users_app:code',
                kwargs={'pk':usuario.id}
            )
        )


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
            'users_app:user_login'
            )
        )


class ChangePassword(LoginRequiredMixin, FormView):
    template_name = 'users/update_pass.html'
    form_class = UpdateFormPass
    success_url = reverse_lazy('users_app:user_login')
    login_url = reverse_lazy('users_app:user_login')

    def form_valid(self, form):
        #para recuperar a un usuario activo
        #esto funciona en cualquier parte del codigo
        my_user = self.request.user        
        new_pass = form.cleaned_data['password1']
        user = authenticate(
            username = my_user,
            password = form.cleaned_data['password'],
        )
        
        if user:
           
            my_user.set_password(new_pass)
            my_user.save()

        logout(self.request)
        

        return super(ChangePassword, self).form_valid(form)

class codeVerification(FormView):
    template_name = 'users/verification.html'
    form_class = Verification
    success_url = reverse_lazy('users_app:user_login')

    #REESCRIBIMOS FUNCIONES PARA QUE FORMS PUEDA TRABAJR CON VIEWS
    def get_form_kwargs(self):
        kwargs = super(codeVerification, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk'],
        }) 
        return kwargs
    def form_valid(self, form):
        User.objects.filter(
            id = self.kwargs['pk']
        ).update(
            is_active=True
        )
        return super(codeVerification, self).form_valid(form)