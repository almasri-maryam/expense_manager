from rest_framework import serializers
from .models import Income, Expense, IncomeCategory, ExpenseCategory

class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = ['id', 'name']

    def validate_name(self, value):
        user = self.context['request'].user
        if IncomeCategory.objects.filter(user=user, name__iexact=value).exists():
            raise serializers.ValidationError("This category already exists. Please choose a different name.")
        return value

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'expense_limit']

    def validate_name(self, value):
        user = self.context['request'].user
        if ExpenseCategory.objects.filter(user=user, name__iexact=value).exists():
            raise serializers.ValidationError("This category already exists. Please choose a different name.")
        return value

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'amount', 'date', 'category', 'description']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'date', 'category', 'is_recurring', 'description']
