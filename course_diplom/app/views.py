from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth.models import Group, User
from .serializers import UserSerializer, GroupSerializer
from app.models import Category, CustomUser, Item, Order, ItemInfo, OrderInfo, Shop, Parameter, ItemParameter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
