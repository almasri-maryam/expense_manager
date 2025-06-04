from rest_framework.exceptions import ValidationError
from ..models import Transaction
from django.db.models import Sum
from dateutil.relativedelta import relativedelta

class TransactionService:
    def __init__(self, user):
        self.user = user

    def validate_limit(self, category, amount, date):
        if category.type == 'expense' and category.expense_limit is not None:
            total = Transaction.objects.filter(
                user=self.user,
                category=category,
                date__year=date.year,
                date__month=date.month
            ).aggregate(Sum("amount"))['amount__sum'] or 0
            if total + amount > category.expense_limit:
                raise ValidationError(
                    f"Adding this expense exceeds the limit for category '{category.name}' ({category.expense_limit})."
                )

    def create(self, data):
        category = data['category']
        amount = data['amount']
        date = data['date']
        self.validate_limit(category, amount, date)
        transaction = Transaction.objects.create(user=self.user, **data)
        if data.get("is_recurring") and category.type == 'expense':
            # إنشاء تكرار شهري تلقائي للنفقات فقط
            Transaction.objects.create(
                user=self.user,
                amount=amount,
                date=date + relativedelta(months=1),
                category=category,
                is_recurring=True,
                transaction_type=category.type,
                description=data.get('description', '')
            )
        return transaction

    def update(self, instance, data):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
