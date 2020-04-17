from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('password', 'email', 'first_name', 'last_name', 'middle_name', 'company', 'position', 'type',)
