from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from .models import User
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,  login
# Create your views here.



class UserView(APIView):
    serializer_class=UserSerializer
    def get(self, request):
        users=User.objects.all()
        serializer=UserSerializer(users, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            registered=serializer.save()
            refresh=RefreshToken.for_user(registered)
            token=refresh.access_token
            return Response({
                        'status': 'success',
                        'message': 'Registration successful',
                        'data': {
                            'access': str(token)
                        },
                        'user': serializer.data

                    }, status=status.HTTP_201_CREATED)
        errors=[]
        if User.objects.filter(email=request.data['email']).exists():
            
            errors.append({
                'field': 'email',
                'message': 'email already exists'
            })
        print(request.data)
        if not request.data['password']:
            errors.append({
                'field': 'password',
                'message': 'password cannot be null'
            })
        if not request.data['firstName']:
            errors.append({
                'field': 'first name',
                'message': 'first name cannot be null'
            })
        if not request.data['lastName']:
            errors.append({
                'field': 'last name',
                'message': 'last name cannot be null'
            })

        return Response({
            'errors':errors
        })
class LoginView(APIView):
    serializer_class=LoginSerializer
    def post(self, request):
        login_user=User.objects.filter(email=request.data['email'])
        if login_user.exists():
            if check_password(request.data['password'], login_user[0].password):
                serializer=UserSerializer(User.objects.get(email=request.data['email']))
                return Response(
                    
                )
