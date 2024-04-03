from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics, decorators, status, permissions
from rest_framework.response import Response
from .serializers import DirectorSerializer, CustomerAuthSerializer, DirectorAuthSerializer, AdminAuthSerializer
from .models import Director
from .throttlings import Anon5ForMinute, User10ForMinute

# Create your views here.


class DirectorListAV(generics.ListCreateAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class DirectorDetailAV(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()



@decorators.api_view(['POST'])
def customer_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user and hasattr(user, 'customer'):
        serializer = CustomerAuthSerializer(user.customer)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)



@decorators.api_view(['POST'])
def customer_register(request):
    serializer = CustomerAuthSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


@decorators.api_view(['POST'])
@decorators.throttle_classes([Anon5ForMinute])
def director_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user and hasattr(user, 'director'):
        serializer = DirectorAuthSerializer(user.director)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@decorators.api_view(['POST'])
def director_register(request):
    serializer = DirectorAuthSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



@decorators.api_view(['POST'])
def admin_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user and user.is_superuser:
        serializer = AdminAuthSerializer(user)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)