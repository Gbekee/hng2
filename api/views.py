from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer, OrgSerializer
from .models import User, Organisation
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,  login
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
class RegisterView(APIView):
    serializer_class=UserSerializer
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
            token=RefreshToken.for_user(login_user.first())
            return Response({
                'status': 'success',
                'message':'Login successful',
                'data':{
                    'access':str(token.access_token)
                },
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Bad request',
            'message':'Authentication failed',
            'statusCode':401
        },  status=status.HTTP_401_UNAUTHORIZED)

class UserView(APIView):
    serializer_class=UserSerializer
    def get(self, request, pk):
        user=User.objects.get(id=pk)
        serializer=UserSerializer(user)
        return Response({
            'status':'Success',
            'message':'<message>',
            'data':serializer.data
        }, status=status.HTTP_200_OK)
class OrgView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=OrgSerializer
    def get(self, request):
        queryset=Organisation.objects.filter(user=request.user)
        serializer=OrgSerializer(queryset, many=True)
        return Response({
            'status':'success',
            'message':'<message>',
            'organisations':serializer.data
        }, status=status.HTTP_200_OK)
    def post(self, request):
        try:
            if 'description' not in request.data:
                neworg=Organisation.objects.create(name= request.data['name'])
            else:
                neworg=Organisation.objects.create(name= request.data['name'], description=request.data['description'])
            neworg.user.add(request.user)
            serializer=OrgSerializer(neworg)
            return Response({
                'status':'success',
                'message':'organisation created successfully',
                'data':serializer.data
                })
        except:
            return Response({
                'status':'Bad request',
                'message':'Client error',
                'statuscode':400
            })
class OrgDetailView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=OrgSerializer
    def get(self, request, pk):
        qs=Organisation.objects.get(id=pk)
        serializer=OrgSerializer(qs)
        return Response({
            'status':'success',
            'message': '<message>',
            'data': serializer.data,
        })
@method_decorator(csrf_exempt, name='dispatch')
class AddUserView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=OrgSerializer
    def post(self, request, pk):
        try:
            Organisation.objects.get(id=pk).user.add(User.objects.get(id=request.data['userId']))
            return Response({
                'status':'Success',
                'message':'user added to organisation successfully'
            })
        except:
            pass