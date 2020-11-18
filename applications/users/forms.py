from django import forms
from django.contrib.auth import authenticate
from .models import User
#from .managers import code_validation

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña'
            }
        )
    )

    password2 = forms.CharField(
        label='Confirma tu contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Confirma Contraseña'
            }
        )
    )
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'geneder'

        )

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2','Las contraseñas no son iguales')
        if len(self.cleaned_data['password1']) <= 8:
            self.add_error('password1','La contraseña debe ser mayor a 8 caracteres')



class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Usuario',
                'style': '{margin: 10px }'
            }
        )
    )

    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Usuario o contraseña incorrectos")
        return self.cleaned_data


class UpdateFormPass(forms.Form):
    password = forms.CharField(
        label='Contraseña Actual',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña Actual'
            }
        )
    )
    password1= forms.CharField(
        label='Nueva contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Nueva contraseña'
            }
        )
    )
    password2= forms.CharField(
        label='Nueva contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Nueva contraseña'
            }
        )
    )
    def clean_password2(self):
        passw = self.cleaned_data['password']
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        
        if passw == pass2:
            self.add_error('password','La contraseña nueva debe de ser diferente a la anterior')
        if pass1 != pass2:
            self.add_error('password2','Las contraseñas no son iguales')
        if len(pass1) <= 6:
            self.add_error('password1','La contraseña debe ser mayor a 8 caracteres')

class Verification(forms.Form):
    code = forms.CharField(required=True)


    #para cargar el kwars que viene de las vistas
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(Verification, self).__init__(*args, **kwargs)
    
    #validar  un campo de formulario usamos clea
    def clean_code(self):
        codigo = self.cleaned_data['code']
        if len(codigo) == 6:
            #verificamos si el codigo y el id son validos
            active = User.objects.code_validation(
                self.id_user,
                codigo
            )
            if not active:
                raise forms.ValidationError("Codigo incorrecto")
        else:
            raise forms.ValidationError("Codigo incorrecto")
