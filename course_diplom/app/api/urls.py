from django.urls import path, include
from ..api.views import UserViewSet, CustomLoginView, ItemViewSet, CategoryViewSet, ShopViewSet, ContactsViewSet
# from rest_framework import routers
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename="user")
router.register(r'items', ItemViewSet, basename="item")
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'shops', ShopViewSet, basename='shop')

users_router = routers.NestedSimpleRouter(router, r'users', lookup='usercontact')
users_router.register(r'contacts', ContactsViewSet, basename="contacts")
# app_name = 'app'

urlpatterns = router.urls + users_router.urls + [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('/', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
]
