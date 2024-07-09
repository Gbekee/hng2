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



class RegisterView(APIView):
    serializer_class=UserSerializer
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            registered=serializer.save()
            # refresh=RefreshToken.for_user(registered)
            # token=refresh.access_token
            return Response({
                        'status': 'success',
                        'message': 'Registration successful',
                        'data': {
                            'access': ''
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
        if len(errors)<1:
            return Response({
                'status':'Bad Request',
                'message':'Registration Unsuccessful',
                'statuscode':400
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'errors':errors
        })
class LoginView(APIView):
    serializer_class=LoginSerializer
    def post(self, request):
        login_user=User.objects.filter(email=request.data['email'])
        if login_user.exists() and login_user.first().check_password(request.data['password']):
            serializer=UserSerializer(User.objects.get(email=request.data['email']))
            return Response({
                'status': 'success',
                'message':'Login successful',
                'data':{
                },
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Bad request',
            'message':'Authentication failed',
            'statusCode':401
        },  status=status.HTTP_401_UNAUTHORIZED)