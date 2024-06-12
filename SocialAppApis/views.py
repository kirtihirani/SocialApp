from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from .models import User
from .serializers import UserSerializer, FriendSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination
from .filters import UserFilter
from rest_framework.decorators import action

# Create your views here.
class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLogin(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = username, password=password)
        if user:
            login(request,user)
            token,created = Token.objects.get_or_create(user = user)
            return Response({'message':'Logged in successfully','token': token.key})
        else:
            return Response({'error':'Invalid Credentials'},status= status.HTTP_401_UNAUTHORIZED)

class UserLogout(generics.GenericAPIView):
    queryset = Token.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response({"Message":"Logged out successfully" ,"status":204},status=204)
    
class UserViewSet(GenericViewSet,generics.RetrieveAPIView, generics.ListAPIView, generics.UpdateAPIView):
    serializer_class = UserSerializer
    model = User
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class= PageNumberPagination
    pagination_class.page_size = 10
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter


    @action(detail=False, methods=['get'], url_path="friends")
    def listAllFriends(self, request):
        userid = request.user.id
        currentUser =  self.queryset.filter(pk = userid).first()
        friendList = currentUser.friends.all()
        serializer = FriendSerializer(friendList, many=True) 
        return Response({"Friends":serializer.data})


   