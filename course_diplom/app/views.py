from django.shortcuts import render
from django.contrib.auth import get_user_model
from app.models import CustomUser
from .forms import RegistrationForm

def signup(request):
    User = get_user_model()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form.Meta.model = CustomUser
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            middle_name = form.cleaned_data.get('middle_name')
            company = form.cleaned_data.get('company')
            position = form.cleaned_data.get('position')
            type = form.cleaned_data.get('type')
            CustomUser.objects.create_user(email, password, first_name, last_name, middle_name, company, position, type)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)


