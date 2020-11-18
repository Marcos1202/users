from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    CHOISE_GENDER = (
        ('M', 'MASCULINO'),
        ('F', 'FEMENINO'),
        ('O', 'OTROS'),
    )
    
    username = models.CharField( max_length=10, unique=True)
    email = models.EmailField()
    first_name = models.CharField("Nombres", max_length=30, blank=True)
    last_name = models.CharField("Apellidos", max_length=30, blank=True)
    geneder = models.CharField("Género", max_length=50,choices=CHOISE_GENDER, blank=True)
    code_register = models.CharField(max_length=6, blank=True)
    is_staff = models.BooleanField("Es staff",default=False)
    is_active = models.BooleanField(default=False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()
    
    def get_short_name(self):
        return self.username

        

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    
