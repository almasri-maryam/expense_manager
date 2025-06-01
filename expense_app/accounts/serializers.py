from rest_framework import serializers
from .models import User, EmailVerification
from .utils import generate_code, send_verification_email


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'cash_currency' ,'password' , 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = generate_code()
        EmailVerification.objects.create(user=user, code=code)
        send_verification_email(user.email, code)
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            verification = EmailVerification.objects.filter(user=user, code=data['code']).latest('created_at')
            user.is_active = True
            user.save()
        except Exception:
            raise serializers.ValidationError("Invalid code")
        return data




class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active', 'is_staff', 'date_joined']


class AdminCreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'is_active']  
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data.pop('is_staff', None)
        user = User.objects.create_user(**validated_data)
        user.is_staff = False  
        user.save()
        return user


