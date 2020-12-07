from django.urls import path, include
from ..api.views import UserViewSet, CustomLoginView, ItemViewSet, CategoryViewSet, ShopViewSet, ContactsViewSet,\
    ItemInfoViewSet
# from rest_framework import routers
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename="user-list")
router.register(r'items', ItemInfoViewSet, basename="item-list")
router.register(r'categories', CategoryViewSet, basename='category-list')
router.register(r'shops', ShopViewSet, basename='shop-list')
# router.register(r'iteminfos', ItemInfoViewSet, basename='iteminfo_basename')

users_router = routers.NestedSimpleRouter(router, r'users', lookup='email')   # этот лукап нужен в кверисете, чтобы передать в фильтр нужный email
users_router.register(r'contacts', ContactsViewSet, basename="user-contacts") # 'basename' is optional. Needed only if the same viewset
                                                                               # is registered more than once.
# app_name = 'app'

urlpatterns = router.urls + users_router.urls + [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('/', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
]
