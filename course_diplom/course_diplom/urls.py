"""course_diplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from app.views import signup
from allauth.account.views import TemplateView
from django.views.generic import RedirectView
from django.conf.urls import url
from rest_auth.registration.views import VerifyEmailView, ConfirmEmailView, RegisterView



urlpatterns = [
    url(r'^verify-email/$', VerifyEmailView.as_view(), name='rest_verify_email'),

    # This url is used by django-allauth and empty TemplateView is
    # defined just to allow reverse() call inside app, for example when email
    # with verification link is being sent, then it's required to render email
    # content.

    # account_confirm_email - You should override this view to handle it in
    # your API client somehow and then, send post to /verify-email/ endpoint
    # with proper key.
    # If you don't want to use API on that step, then just use ConfirmEmailView
    # view from:
    # django-allauth https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py
    url('api/registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    # re_path("r'^verifyemail/(?P<key>\w+)$", ConfirmEmailView.as_view(), name='account_confirm_email'),
    # path('api/users', UserView.as_view({'get': 'list'})),
    # path('api/users/<int:pk>', UserView.as_view({'get': 'retrieve'})),
    # path('api/groups', GroupViewSet.as_view()),
    # path('api/', include('rest_framework.urls', namespace='rest_framework'))

    # REST FRAMEWORK URLS
    path('api/v1/', include('app.api.urls')),
]

