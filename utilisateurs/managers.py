# filepath: /home/aro/Mizara/mizara/utilisateurs/managers.py
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, numero_telephone, password=None, **extra_fields):
        if not numero_telephone:
            raise ValueError('The Numero Telephone field must be set')
        
        # S'assurer que le champ username n'est pas défini
        if 'username' in extra_fields:
            extra_fields.pop('username')
            
        # Normaliser l'email s'il est fourni
        email = extra_fields.get('email', '')
        if email:
            email = self.normalize_email(email)
            extra_fields['email'] = email
            
        # Créer l'utilisateur avec le numéro de téléphone comme identifiant
        user = self.model(numero_telephone=numero_telephone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def authenticate(self, **kwargs):
        # Gérer l'authentification par email ou numéro de téléphone
        identifier = kwargs.get('email') or kwargs.get('numero_telephone')
        password = kwargs.get('password')
        
        if not identifier or not password:
            return None
            
        try:
            if '@' in identifier:  # Authentification par email
                user = self.get(email=identifier)
            else:  # Authentification par numéro de téléphone
                user = self.get(numero_telephone=identifier)
        except User.DoesNotExist:
            return None
            
        if user.check_password(password):
            return user
        return None

    def create_superuser(self, numero_telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # S'assurer que le champ username n'est pas défini
        if 'username' in extra_fields:
            extra_fields.pop('username')
            
        return self.create_user(numero_telephone, password, **extra_fields)
