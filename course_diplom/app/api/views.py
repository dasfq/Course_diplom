from rest_framework import viewsets
from app.api.serializers import CustomUserSerializer, CustomLoginSerializer, ItemSerializer, CategorySerializer, ShopSerializer
from app.models import CustomUser, Item, ItemInfo, Category, Shop
from rest_auth.views import LoginView
from rest_auth.serializers import LoginSerializer
from rest_framework import request

class CustomLoginView(LoginView):
    serializer_class = LoginSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # lookup_field = 'email'

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

    # def list(self, request):
    #     queryset = User.objects.all()
    #     serializer_class = UserSerializer(queryset, many=True)
    #     return Response(serializer_class.data)
    #
    # def retrieve(self, request, pk=0):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer_class = UserSerializer(user)
    #     return Response(serializer_class.data)

    #
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # lookup_field = ('username', 'password', 'email', 'groups',)
    #
    # def get(self, request, *args, **kwargs):
    #     serializer = UserSerializer(User.objects.all(), many=True)
    #     return Response(serializer.data)
    #
    # def post(self, request, *args, **kwargs):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)

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