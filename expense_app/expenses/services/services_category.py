from ..models import IncomeCategory, ExpenseCategory
from rest_framework.exceptions import ValidationError

class CategoryService:
    def __init__(self, user):
        self.user = user

    def create_income_category(self, data):
        if IncomeCategory.objects.filter(user=self.user, name__iexact=data['name']).exists():
            raise ValidationError("This income category already exists.")
        return IncomeCategory.objects.create(user=self.user, **data)

    def update_income_category(self, instance, data):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete_income_category(self, instance):
        instance.delete()

    def create_expense_category(self, data):
        if ExpenseCategory.objects.filter(user=self.user, name__iexact=data['name']).exists():
            raise ValidationError("This expense category already exists.")
        return ExpenseCategory.objects.create(user=self.user, **data)

    def update_expense_category(self, instance, data):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete_expense_category(self, instance):
        instance.delete()