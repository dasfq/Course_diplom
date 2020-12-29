from django.urls import path, include
from ..api.views import UserViewSet, CustomLoginView, ItemViewSet, CategoryViewSet, ShopViewSet, ContactsViewSet,\
    ItemInfoViewSet, ParameterViewSet, SupplierUpdate, ItemParamsViewSet, StatusUpdate, BasketView, OrderViewSet,\
    LogoutView
# from rest_framework import routers
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename="users")
router.register(r'items', ItemInfoViewSet, basename="items")
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'shops', ShopViewSet, basename='suppliers')
router.register(r'parameters', ParameterViewSet, basename='parameters')
router.register(r'itemparams', ItemParamsViewSet, basename='item-params')
router.register(r'orders', OrderViewSet, basename='orders')

users_router = routers.NestedSimpleRouter(router, r'users', lookup='email')   # этот лукап нужен в кверисете, чтобы передать в фильтр нужный email
users_router.register(r'contacts', ContactsViewSet, basename="user-contacts") # 'basename' is optional. Needed only if the same viewset
                                                                               # is registered more than once.
# app_name = 'app'

urlpatterns = router.urls + users_router.urls + [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('/', include('rest_auth.urls')),
    path('supplier/update/', SupplierUpdate.as_view(), name='update-items'),
    path('supplier/status/', StatusUpdate.as_view(), name='update-status'),
    path('basket/', BasketView.as_view(), name = "basket"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('makeorder/', OrderViewSet.as_view({"post":"create"}), name='makeorder'),
]