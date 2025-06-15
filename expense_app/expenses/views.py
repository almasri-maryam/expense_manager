from rest_framework import viewsets
from expense_app.accounts.permissions import IsRegularUserOnly
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer
from .services.services_category import CategoryService
from .services.services_transiction import TransactionService

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .profile  import UserProfile


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsRegularUserOnly]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        category = CategoryService(self.request.user).create(serializer.validated_data)
        serializer.instance = category

    def perform_update(self, serializer):
        category = CategoryService(self.request.user).update(self.get_object(), serializer.validated_data)
        serializer.instance = category

    def perform_destroy(self, instance):
        CategoryService(self.request.user).delete(instance)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsRegularUserOnly]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        transaction = TransactionService(self.request.user).create(serializer.validated_data)
        serializer.instance = transaction

    def perform_update(self, serializer):
        transaction = TransactionService(self.request.user).update(self.get_object(), serializer.validated_data)
        serializer.instance = transaction

    def perform_destroy(self, instance):
        TransactionService(self.request.user).delete(instance)


@api_view(['POST'])
@permission_classes([IsRegularUserOnly])
def set_fcm_token(request):
    token = request.data.get('fcm_token')
    if not token:
        return Response({"error": "Missing token"}, status=400)

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.fcm_token = token
    profile.save()

    return Response({"message": "Token saved successfully"})

