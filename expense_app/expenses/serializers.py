from rest_framework import serializers
from .models import Category, Transaction

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type']

    def validate_name(self, value):
        user = self.context['request'].user
        category_type = self.initial_data.get('type')
        if Category.objects.filter(user=user, name__iexact=value, type=category_type).exists():
            raise serializers.ValidationError("This category already exists for this type. Please choose a different name.")
        return value


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'date', 'category', 'transaction_type', 'description', 'is_recurring']

    def validate(self, data):
        category = data.get('category')
        transaction_type = data.get('transaction_type')
        if category.type != transaction_type:
            raise serializers.ValidationError("Transaction type must match the category type.")
        return data
