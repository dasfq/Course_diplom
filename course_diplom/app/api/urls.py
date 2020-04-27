from django.urls import path, include
from ..api.views import UserViewSet, CustomLoginView, ItemViewSet, CategoryViewSet, ShopViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename="user")
router.register(r'items', ItemViewSet, basename="item")
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'shops', ShopViewSet, basename='shop')


# app_name = 'app'

urlpatterns = router.urls + [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('/', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
]
