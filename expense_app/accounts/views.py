
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.exceptions import ValidationError
from .serializers import RegisterSerializer, VerifyEmailSerializer, AdminUserSerializer, AdminCreateUserSerializer
from .models import User
from .services import (
    register_user, verify_email, login_user, logout_user,
    change_password, get_user_profile, delete_user_account
)

from .permissions import IsAdmin, IsRegularUserOnly

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        result = register_user(serializer)
        return Response(result, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        result = verify_email(serializer)
        return Response(result)



class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        result = login_user(email, password, is_admin=False)
        return Response(result)


class AdminLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        result = login_user(email, password, is_admin=True)
        return Response(result)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        result = logout_user(refresh_token)
        return Response(result)


class ChangePasswordView(APIView):
    permission_classes = [IsRegularUserOnly]  

    def post(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        new_password_confirm = request.data.get("new_password_confirm")

        if not old_password or not new_password or not new_password_confirm:
            return Response(
                {"error": "Old password, new password and confirmation are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if new_password != new_password_confirm:
            return Response(
                {"error": "New passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = change_password(
                user=request.user,
                old_password=old_password,
                new_password=new_password
            )
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsRegularUserOnly]

    def get(self, request):
        result = get_user_profile(request.user)
        return Response(result)


class DeleteAccountView(APIView):
    permission_classes = [IsRegularUserOnly]

    def delete(self, request):
        result = delete_user_account(request.user)
        return Response(result)


class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class AdminCreateUserView(generics.CreateAPIView):
    serializer_class = AdminCreateUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        serializer.save(is_staff=False)


class AdminDeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_staff:
            return Response({"error": "Admin users cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

