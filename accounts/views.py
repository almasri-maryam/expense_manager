from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from rest_framework import generics


from .serializers import (
    RegisterSerializer, VerifyEmailSerializer,
    AdminUserSerializer, AdminCreateUserSerializer
)
from .models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class IsRegularUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "account created , check your email"}, status=201)
        return Response(serializer.errors, status=400)



class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "verified successfully"})
        return Response(serializer.errors, status=400)



class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None and not user.is_staff:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "role": "user",
                "message": "you are logged in"
            })
        return Response({"error": "invalid login data "}, status=status.HTTP_401_UNAUTHORIZED)


class AdminLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_staff:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "role": "admin",
                "message": "you are logged in"
            })
        return Response({"error": "invalid login data"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": " you are logged out "})
        except Exception:
            return Response({"error": "invalid logout "}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsRegularUserOnly]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "the old pass is not correct"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "pass changed success "}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    permission_classes = [IsRegularUserOnly]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
        }
        return Response(data)


class DeleteAccountView(APIView):
    permission_classes = [IsRegularUserOnly]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"detail": " the account has been successfully deleted "})




class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class AdminCreateUserView(generics.CreateAPIView):
    serializer_class = AdminCreateUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        serializer.save(is_staff=False)


from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

class AdminDeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_staff:
            return Response({"error": "لA user with administrator privileges cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
