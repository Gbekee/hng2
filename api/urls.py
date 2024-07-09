from django.urls import path
from .views import UserView, LoginView, RegisterView
urlpatterns=[
    path('auth/register/', RegisterView.as_view(), name='users'),
    path('auth/login/', LoginView.as_view(), name='login')
]