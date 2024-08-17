# urls.py
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserUpdateView, ChangePasswordView, isActivate, UserLogoutView, UserListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('active/<uid64>/<token>', isActivate, name='active'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
