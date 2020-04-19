from rest_framework import serializers
from django.contrib.auth.models import Group
from app.models import CustomUser
from rest_auth import serializers as auth_serializers


class CustomUserSerializer(auth_serializers.UserDetailsSerializer):

    class Meta:
        model = CustomUser
        fields = ('password', 'email', 'first_name', 'last_name', 'middle_name', 'company', 'position', 'type',)

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)