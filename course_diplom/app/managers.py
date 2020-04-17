from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, first_name, last_name, middle_name, company, position, type):
        if not email:
            raise ValueError('Provide email')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, middle_name=middle_name, company=company, position=position,type=type)
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

        return self.create_user(email, password, **extra_fields)

