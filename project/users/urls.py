from django.urls import path
from .views import (
    UserRetrieveUpdateDestroyView,  
    UserLoginView,
    UserCreateView,
    UserListCreateView
)

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),  # User registration
    path('login/', UserLoginView.as_view(), name='user-login'),         # User login
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),  # User detail, update, delete
    path('users/', UserListCreateView.as_view(), name='user-list-create'),  # User list and create
]