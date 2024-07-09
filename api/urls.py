from django.urls import path
from .views import UserView, LoginView
urlpatterns=[
    path('auth/register', UserView.as_view(), name='users'),
    path('login', LoginView.as_view(), name='login')
]