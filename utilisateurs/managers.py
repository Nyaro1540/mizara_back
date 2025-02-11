# filepath: /home/aro/Mizara/mizara/utilisateurs/managers.py
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, numero_telephone, password=None, **extra_fields):
        if not numero_telephone:
            raise ValueError('The Numero Telephone field must be set')
        user = self.model(numero_telephone=numero_telephone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, numero_telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(numero_telephone, password, **extra_fields)