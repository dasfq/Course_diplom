from rest_framework import viewsets, response
from app.api.serializers import CustomUserSerializer, CustomLoginSerializer, ItemSerializer, CategorySerializer, ShopSerializer, ContactSerializer
from app.models import CustomUser, Item, ItemInfo, Category, Shop, Contact
from rest_auth.views import LoginView
from rest_auth.serializers import LoginSerializer
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


    ## не получилось. методы post, put содержали поля для users, а не для contacts. ПОэтому буду делать через nested routers.
    # @action(methods=['get', 'post', 'put', 'destroy'], detail=True, url_name='contacts', url_path='contacts')
    # def contacts(self, request, pk=None):
    #     contact = Contact.objects.filter(user__pk=pk)
    #     serializer = ContactSerializer(contact, many=True)
    #     return response.Response(serializer.data)

class ContactsViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = Contact.objects.filter(user__email=self.kwargs['usercontact_email'])
        return queryset

    def create(self, request, *args, **kwargs):
        user_email = self.kwargs['usercontact_email']
        user = CustomUser.objects.get(email=user_email)
        serializer = ContactSerializer(data=request.data) ## если здесь добавим user, то в сериализаторе
                                                          ## вызовется метод update. Поэтому user передадим
                                                          ## далее в методе save()
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        print('12312312321')
        instance.delete()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        shop_id = self.request.query_params.get('shop_id', None)
        category_id = self.request.query_params.get('category_id', None)
        queryset = Shop.objects.filter(id=shop_id,
                                      category__id=category_id)
        return queryset



class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()

#
# class GroupViewSet(APIView):
#     # authentication_classes = AllowAny
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     # lookup_field = ('name',)
#
#     def get(self, request, *args, **kwargs):
#         serializer = GroupSerializer(Group.objects.all(), many=True)
#         return Response(serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         serializer = GroupSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
#
#
#