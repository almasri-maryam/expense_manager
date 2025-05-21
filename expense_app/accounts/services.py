# services.py

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken


def register_user(serializer):
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return {"message": "Account created. Please check your email."}

def verify_email(serializer):
    if serializer.is_valid(raise_exception=True):
        return {"message": "Email verified successfully."}
    


def login_user(email, password, is_admin=False):
    user = authenticate(email=email, password=password)
    if user is None:
        raise AuthenticationFailed("Invalid login credentials.")
    
    if is_admin and not user.is_staff:
        raise AuthenticationFailed("You are not authorized as admin.")
    if not is_admin and user.is_staff:
        raise AuthenticationFailed("You are not authorized as a regular user.")

    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "role": "admin" if user.is_staff else "user",
        "message": "You are logged in successfully."
    }

def logout_user(refresh_token):
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return {"message": "You are logged out successfully."}
    except Exception:
        raise ValidationError("Invalid logout attempt.")

def change_password(user, old_password, new_password):
    if not user.check_password(old_password):
        raise ValidationError({"error": "Old password is incorrect."})
    user.set_password(new_password)
    user.save()
    return {"message": "Password changed successfully."}

def get_user_profile(user):
    return {
        "username": user.username,
        "email": user.email
    }

def delete_user_account(user):
    user.delete()
    return {"message": "Your account has been deleted successfully."}

