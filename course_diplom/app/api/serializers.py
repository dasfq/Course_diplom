from rest_framework import serializers
from django.contrib.auth.models import Group
from app.models import CustomUser, Item, ItemInfo, Category, Shop, Contact
from rest_auth import serializers as auth_serializers
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email


class CustomLoginSerializer(auth_serializers.LoginSerializer):
    username = serializers.HiddenField(default='')


class CustomRegisterSerializer(RegisterSerializer, serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, label='Пароль')
    password2 = serializers.CharField(write_only=True, label='Повтор пароля')
    middle_name = serializers.CharField(required=True, write_only=True)
    company = serializers.CharField(required=True, write_only=True)
    position = serializers.CharField(required=True, write_only=True)

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'middle_name': self.validated_data.get('middle_name', ''),
            'company': self.validated_data.get('company', ''),
            'position': self.validated_data.get('position', ''),
            'type': self.validated_data.get('type', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        user.__setattr__('middle_name', self.cleaned_data.get('middle_name'))
        user.__setattr__('company', self.cleaned_data.get('company'))
        user.__setattr__('position', self.cleaned_data.get('position'))
        user.__setattr__('type', self.cleaned_data.get('type'))
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'middle_name', 'company', 'position', 'type',)

class CustomUserSerializer(auth_serializers.UserDetailsSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk', 'email', 'password', 'first_name', 'last_name', 'middle_name', 'company', 'position', 'type', 'contact_set')
        depth = 1


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('pk','name',)


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('pk', 'category', 'name',)
        extra_kwargs = {
            'category': {'view_name': 'category-detail', 'lookup_field': 'pk'}
        }

class ShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = ('pk', 'name', 'url', 'is_active', 'category',)
        extra_kwargs = {
            'category': {'lookup_field': 'pk'}
        }

class ContactSerializer(serializers.ModelSerializer):


    def create(self, validated_data):
        contact = Contact(adress=validated_data['adress'], phone=validated_data['phone'])
        contact.save()
        user = validated_data['user']  ## здесь юзера берём из val_data, т.к. во вьё передали через метод save()
        contact.user.add(user)
        return contact

    class Meta:
        model = Contact
        fields = ('adress', 'phone', 'pk',)