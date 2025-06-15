from django.urls import path
from .views import (
    RegisterView, VerifyEmailView,
    UserLoginView, AdminLoginView, LogoutView,
    ChangePasswordView, UserProfileView, DeleteAccountView,
    AdminUserListView, AdminCreateUserView, AdminDeleteUserView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),

    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/create/', AdminCreateUserView.as_view(), name='admin-user-create'),
    path('admin/users/<int:pk>/delete/', AdminDeleteUserView.as_view(), name='admin-user-delete'),    
]
