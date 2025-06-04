from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer
from .services.services_category import CategoryService
from .services.services_transactions import TransactionService

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
