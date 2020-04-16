from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import Group, User
from course_diplom.serializers import UserSerializer, GroupSerializer

class UserViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = ('username', 'password', 'email', 'groups',)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class GroupViewSet(APIView):
    # authentication_classes = AllowAny
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # lookup_field = ('name',)

    def get(self, request, *args, **kwargs):
        serializer = GroupSerializer(Group.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)




