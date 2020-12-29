from rest_framework import viewsets, response, mixins
from rest_framework.views import APIView
from app.api.serializers import CustomUserSerializer, CustomLoginSerializer, ItemSerializer,\
    CategorySerializer, ShopSerializer, ContactSerializer, ItemInfoSerializer, ParameterSerializer,\
    ItemParamsSerializer, BasketSerializer
from app.models import CustomUser, Item, ItemInfo, Category, Shop, Contact, Parameter, ItemParameter, Order, OrderInfo
from rest_auth.views import LoginView, LogoutView
from rest_auth.serializers import LoginSerializer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import requests
import yaml
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from json import loads as load_json

from rest_framework.decorators import action

## пока не используется
class CustomLoginView(LoginView):
    serializer_class = LoginSerializer
##

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'email'
    lookup_value_regex = '[\w@.]+'

    def list(self, request, *args, **kwargs):
        print(self.queryset)
        current_user = request.user.id
        serializer = CustomUserSerializer(self.queryset, many=True)
        return JsonResponse({'current_user': current_user, 'users_list': serializer.data})

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
    queryset = Item.objects.all()

    # Этот метод, если нужно удалитьт все Item
    # def destroy(self, *args, **kwargs):
    #     Item.objects.all().delete()
    #     return JsonResponse()

class ItemInfoViewSet(viewsets.ModelViewSet):
    serializer_class = ItemInfoSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        shop_id = self.request.query_params.get('shop_id', None)
        category_id = self.request.query_params.get('category_id', None)
        if shop_id:
            queryset = ItemInfo.objects.filter(shop__id=shop_id)
        else: queryset = ItemInfo.objects.all()
        if category_id:
            queryset = queryset.filter(item__category__id=category_id)
        return queryset

class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    lookup_field = 'pk'

class ParameterViewSet(viewsets.ModelViewSet):
    serializer_class = ParameterSerializer
    queryset = Parameter.objects.all()

class ItemParamsViewSet(viewsets.ModelViewSet):
    serializer_class = ItemParamsSerializer
    queryset = ItemParameter.objects.all()

class SupplierUpdate(APIView):
    """
    Класс для обновления прайса от поставщика.
    Поставщик подгружает ссылку на сам файл.
    Т.к. это не viewset, то в urls.py прописывается отдельно.
    """
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, "Error": "Log-in required"}, status=403)
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
        shop.url = url
        for category in stream['categories']:
            category_obj, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
            shop.category.add(category_obj)
            shop.save()
            ItemInfo.objects.filter(shop__id=shop.id).delete()
        for item in stream['goods']:
            item_obj, _ = Item.objects.get_or_create(name=item['name'])
            item_obj.category.add(Category.objects.get(id=item['category']))
            item_info_obj, _ = ItemInfo.objects.get_or_create(item=item_obj,
                                                              model=item['model'],
                                                              price=item['price'],
                                                              price_rrc=item['price_rrc'],
                                                              in_stock_qty=item['quantity'],
                                                              external_id=item['id'],
                                                              shop=shop)
            for param_name, value in item['parameters'].items():
                parameter_obj, _ = Parameter.objects.get_or_create(name=param_name)
                ItemParameter.objects.get_or_create(item=item_info_obj,
                                                    parameter=parameter_obj,
                                                    value=value)
        return JsonResponse({"Status": True})

class StatusUpdate(APIView):
    """
    Класс для получения и обновления статуса магазина.
    """

    def shop(self, request, new_status=None):
        shop_id = request.data.get('shop_id')
        shop = Shop.objects.get(id=shop_id)
        if new_status:
            shop.is_active = new_status
        serializer = ShopSerializer(shop)
        return (serializer.data)

    def get(self, request, *args, **kwargs):
        if request.user.type != 'shop':
            return JsonResponse({"Status": False, "Error": "Только для магазинов"})
        if not request.user.is_authenticated:
            return JsonResponse({"Status": False, "Error": "Log-in required"}, status=403)
        data = self.shop(request)
        return JsonResponse(data)                                        # JsonResponse уже содержит в себе json.dumps()

    def post(self, request, *args, **kwargs):
        if request.user.type != 'shop':
            return JsonResponse({"Status": False, "Error": "Только для магазинов"})
        if not request.user.is_authenticated:
            return JsonResponse({"Status": False, "Error": "Log-in required"}, status=403)
        new_status = request.data.get('is_active')
        data = self.shop(request, new_status)
        return JsonResponse(data)

class BasketView(LoginRequiredMixin, mixins.ListModelMixin, APIView):
    # """
    # Класс для добавления управления корзиной
    # """

    def get(self, request, *args, **kwargs):
        orders = OrderInfo.objects.all().filter(order__user_id=request.user.id)
        serializer = BasketSerializer(orders, many = True)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, *args, **kwargs):
        orders=OrderInfo.objects.all().filter(order__user_id=request.user.id)
        orders.delete()
        serializer = BasketSerializer(orders, many = True)
        return JsonResponse(serializer.data, safe=False)


    def post(self, request, *args, **kwargs):
        raw_data = request.data.get('items')
        if raw_data:
            try:
                # data содержит уже dict.
                data = load_json(raw_data)
            except:
                return JsonResponse({"Status1": False, "Error": "Wrong input format"})
            else:
                items_added = 0
                basket, _ = Order.objects.get_or_create(user_id=request.user.id, status='basket')
                for item in data:
                    # добавляем в словарь нужный ключ, под нужный нам вид объекта OrderInfo.
                    item.update({'order': basket.id})
                    order_info, _ = OrderInfo.objects.get_or_create(
                        order_id=basket.id, item_info_id=item['item_info'], defaults={'quantity': 0}
                    )
                    # добавляем в data=item количество из запроса.
                    # Можно было бы и покруче - переопределить в сериалайзере методы update() и там прописать сложение.
                    item['quantity'] += order_info.quantity
                    # когда указан первый аргумент - существующий объект, то сериалайзер при вызове save() его обновит update(),
                    # а не create() новый
                    serializer = BasketSerializer(order_info, data=item)
                    # is_valid создаёт из dict экземпляры моделей.
                    if serializer.is_valid():
                        serializer.save()
                        items_added +=1
                    else:
                        return JsonResponse({"Status3": 'False', "Error": serializer.errors})
                return JsonResponse({"Status4": True, "Добавлено товаров": items_added})
        return JsonResponse({"Status5": False, "Error": "Не все аргументы указаны."})

    def put(self, request, *args, **kwargs):
        # Отличие от POST. POST вызывается со страницы товара. А ПУТ со страницы корзины, когда лишь обновляем цифры.
        raw_data = request.data.get('items')
        if raw_data:
            try:
                data_dict = load_json(raw_data)
            except:
                return JsonResponse({"Status": False, "Error": "Wrong input format"})
            else:
                for item in data_dict:
                    order_item = OrderInfo.objects.filter(id=item['id'])
                    if not order_item:
                        return JsonResponse({"Status": False, "Error": "Такого товара нет в корзине."})
                    order_item.update(quantity=item['quantity'])
                return JsonResponse({"Status": True})
        return JsonResponse({"Status": False, "Error": "Не все аргументы указаны."})


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = BasketSerializer

    def get_queryset(self):                             # для лукапов и связей между моделями используют __
        user_id = self.request.user.id
        orders = OrderInfo.objects.filter(
            order__user_id=user_id
        ).exclude(
            order__status='basket'
        )
        return orders

    def list(self, request, *args, **kwargs):
        return JsonResponse({"Status": True})

    def create(self, request, *args, **kwargs):
        print('creating')
        order = OrderInfo.objects.all().filter(
            order__user_id=request.user.id, order__status='basket'
        )
        if order:
            order.status = 'new'
            serializer = BasketSerializer(order)
            return serializer.data
        else:
            return JsonResponse({'Status': False, 'Error': 'Сначала добавьте товары в корзину'})
        # if serializer.is_valid():
        #     try:
        #         serializer.save()
        #     except IntegrityError as e:
        #         return JsonResponse({'status': False, "Error": str(e)})
        # else:
        #     return JsonResponse({'status': False, "Error": serializer.errors})


#  через APIView
# class OrderView(LoginRequiredMixin, mixins.ListModelMixin, APIView):
#     serializer_class = BasketSerializer
#
#     def get_queryset(self):                             # для лукапов и связей между моделями используют __
#         user_id = self.request.user.id
#         orders = OrderInfo.objects.filter(
#             order__user_id=user_id
#         ).exclude(
#             order__status='basket'
#         )
#         return orders