from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class Usuario(AbstractUser):
    documento = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8,10}$',
                message='El documento debe tener entre 8 y 10 dígitos'
            )
        ]
    )
    
    REQUIRED_FIELDS = ['email', 'documento']
    
    def __str__(self):
        return  self.documento + self.username+' - ' + self.first_name + ' ' + self.last_name
