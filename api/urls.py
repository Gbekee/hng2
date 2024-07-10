from django.urls import path
from .views import UserView, LoginView, RegisterView, OrgView, OrgDetailView, AddUserView
urlpatterns=[
    path('auth/register/', RegisterView.as_view(), name='users'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('api/users/:<str:pk>', UserView.as_view(), name='user'),
    path('api/organisations/', OrgView.as_view(), name='organisations'),
    path('api/organisations/:<str:pk>', OrgDetailView.as_view(), name='organisation_detail'),
    path('api/organisations/:<str:pk>/add-user', AddUserView.as_view(), name='adduser')
]