from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, IncomeViewSet, IncomeCategoryViewSet, ExpenseCategoryViewSet

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'incomes', IncomeViewSet, basename='income')
router.register(r'income-categories', IncomeCategoryViewSet, basename='income-category')
router.register(r'expense-categories', ExpenseCategoryViewSet, basename='expense-category')

urlpatterns = [
    path('', include(router.urls)),
]
