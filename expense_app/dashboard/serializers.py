# dashboard/serializers.py
from rest_framework import serializers

class DashboardSerializer(serializers.Serializer):
    total_expenses = serializers.FloatField()
    total_incomes = serializers.FloatField()
    expenses_by_category = serializers.DictField(child=serializers.FloatField())
    incomes_by_category = serializers.DictField(child=serializers.FloatField())
    expense_trend = serializers.DictField(child=serializers.DictField(child=serializers.FloatField()))
    income_trend = serializers.DictField(child=serializers.DictField(child=serializers.FloatField()))
