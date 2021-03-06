from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import UserManager, BaseUserManager

class CustomUserManager(BaseUserManager):
    '''
    этот менеджер не используется в api.
    это для регистрации через форму, которую я в начале сделал (http://127.0.0.1:8000/signup/).
    А нужно через api
    '''
    def create_user(self, email, password, type, first_name='', last_name='', middle_name='', company='', position='', **extra_fields):
        if not email:
            raise ValueError('Provide email')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, middle_name=middle_name, company=company, position=position,type=type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, type='shop', **extra_fields)

