from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Income, Expense, IncomeCategory, ExpenseCategory
from .serializers import IncomeSerializer, ExpenseSerializer, IncomeCategorySerializer, ExpenseCategorySerializer
from .services.services_incomes import IncomeService
from .services.services_expenses import ExpenseService
from .services.services_category import CategoryService

class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        IncomeService(self.request.user).create(serializer.validated_data)

        

    def perform_update(self, serializer):
        IncomeService(self.request.user).update(self.get_object(), serializer.validated_data)

    def perform_destroy(self, instance):
        IncomeService(self.request.user).delete(instance)

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        ExpenseService(self.request.user).create(serializer.validated_data)

    def perform_update(self, serializer):
        ExpenseService(self.request.user).update(self.get_object(), serializer.validated_data)

    def perform_destroy(self, instance):
        ExpenseService(self.request.user).delete(instance)

class IncomeCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return IncomeCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        CategoryService(self.request.user).create_income_category(serializer.validated_data)

    def perform_update(self, serializer):
        CategoryService(self.request.user).update_income_category(self.get_object(), serializer.validated_data)

    def perform_destroy(self, instance):
        CategoryService(self.request.user).delete_income_category(instance)

class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExpenseCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        CategoryService(self.request.user).create_expense_category(serializer.validated_data)

    def perform_update(self, serializer):
        CategoryService(self.request.user).update_expense_category(self.get_object(), serializer.validated_data)

    def perform_destroy(self, instance):
        CategoryService(self.request.user).delete_expense_category(instance)
