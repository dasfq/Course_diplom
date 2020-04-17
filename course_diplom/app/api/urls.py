from django.urls import path, include
from ..api.views import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename="user")


app_name = 'app'

urlpatterns = router.urls