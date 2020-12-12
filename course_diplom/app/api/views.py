from rest_framework import viewsets, response, status
from rest_framework.views import APIView
from app.api.serializers import CustomUserSerializer, CustomLoginSerializer, ItemSerializer,\
    CategorySerializer, ShopSerializer, ContactSerializer, ItemInfoSerializer, ParameterSerializer
from app.models import CustomUser, Item, ItemInfo, Category, Shop, Contact, Parameter, ItemParameter
from rest_auth.views import LoginView
from rest_auth.serializers import LoginSerializer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests
import yaml
from rest_framework.decorators import action
import json
from django.http import JsonResponse


## пока не используется
class CustomLoginView(LoginView):
    serializer_class = LoginSerializer
##


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'email'
    lookup_value_regex = '[\w@.]+'

class ContactsViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    lookup_field = 'pk'                                  # lookup - это похоже то,что пишем в url:  users/36/

    def get_queryset(self):
        print("1st print", self.kwargs)
        queryset = Contact.objects.filter(user__email=self.kwargs['email_email'])   ##[lookup1_lookup2], где
                                                                                    # lookup1 - это lookup из NestedSimpleRouter
                                                                                    # lookup2 - это lookup_field у UserViewSet
        return queryset

    def create(self, request, *args, **kwargs):
        user_email = self.kwargs['usercontact_email']
        user = CustomUser.objects.get(email=user_email)
        serializer = ContactSerializer(data=request.data) ## если здесь 2м аргументом добавим user, то в сериализаторе
                                                          ## вызовется метод update. Поэтому user передадим
                                                          ## далее в методе save()
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)                        #это отправляет user в метод create сериалайзера, где с ним
                                                            # потом можно работать
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, headers=headers)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        shop_id = self.request.query_params.get('shop_id', None)
        category_id = self.request.query_params.get('category_id', None)
        queryset = Item.objects.filter(iteminfo__shop__id=shop_id,
                                      category__id=category_id)
        return queryset

class ItemInfoViewSet(viewsets.ModelViewSet):
    serializer_class = ItemInfoSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        shop_id = self.request.query_params.get('shop_id', None)
        category_id = self.request.query_params.get('category_id', None)
        queryset = ItemInfo.objects.filter(shop__id=shop_id,
                                      item__category__id=category_id)
        return queryset

class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    lookup_field = 'pk'

class ParameterViewSet(viewsets.ModelViewSet):
    serializer_class = ParameterSerializer
    queryset = Parameter.objects.all()

class SupplierUpdate(APIView):
    """
    Класс для обновления прайса от поставщика.
    Поставщик подгружает ссылку на сам файл.
    Т.к. это не viewset, то в urls.py происывается отдельно.
    """
    def post(self, request, *args, **kwargs):
        if request.user.type != 'shop':
            return JsonResponse({'Status': False, "Error": "Только для магазинов"})
        url = request.data.get('url')
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'status': False, 'Error': str(e)})
            else:
                stream = requests.get(url).content                               # загружает как есть в виде yaml
            stream = yaml.safe_load(stream)                                      # конвертит yaml в JSON
        shop, _ = Shop.objects.get_or_create(name=stream['shop'])
        for category in stream['categories']:
            category_obj, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
            shop.category.add(category_obj)
            shop.save()
            print('создал shop:', shop)
        for item in stream['goods']:
            item_obj, _ = Item.objects.get_or_create(name=item['name'], category__id=item['category'])
            print('создал item:', item_obj)
            item_info_obj, _ = ItemInfo.objects.get_or_create(item=item_obj,
                                                           model=item['model'],
                                                           price=item['price'],
                                                           price_rrc=item['price_rrc'],
                                                           quantity=item['quantity'])
            print('создал item_info:', item_info_obj)
            for parameter in item['parameters'].keys():
                parameter_obj, _ = ItemParameter.objects.get_or_create(item=item_info_obj,
                                                                    parameter=parameter,
                                                                    value=item['parameters']['parameter'])

        print(shop)
        print(new_category)
        return JsonResponse(stream)

