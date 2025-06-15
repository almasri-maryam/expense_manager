from rest_framework.exceptions import ValidationError
from ..models import Transaction
from .services_notification import NotificationService
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.db.models import Sum

class TransactionService:
    def __init__(self, user):
        self.user = user

    def validate_limit(self, category, amount, date):
        if category.type == 'expense' and hasattr(category, 'expense_limit') and category.expense_limit is not None:
            total = Transaction.objects.filter(
                user=self.user,
                category=category,
                date__year=date.year,
                date__month=date.month
            ).aggregate(Sum("amount"))['amount__sum'] or 0

            if total + amount > category.expense_limit:
                token = getattr(self.user.profile, 'fcm_token', None)
                if token:
                    NotificationService(api_key="BMDT5xUkxEpzJzq_JjPYSk9G2C0LmeSkY3qITJdErNVD0ixyD71abhdtnhT-l8lHBERgKFQnuaW6nZHWMv7L6IE").send(
                        token,
                        "Expense Limit Exceeded",
                        f"You exceeded the limit ({category.expense_limit}) for {category.name}."
                    )
                raise ValidationError(
                    f"Adding this expense exceeds the limit for category '{category.name}' ({category.expense_limit})."
                )

    def create(self, data):
        category = data['category']
        amount = data['amount']
        date = data['date']
        self.validate_limit(category, amount, date)

        transaction = Transaction.objects.create(user=self.user, **data)

        if data.get("is_recurring"):
            self.create_next_recurring(transaction)

        return transaction

    def create_next_recurring(self, transaction):
        next_date = transaction.date + relativedelta(months=1)
        exists = Transaction.objects.filter(
            user=transaction.user,
            amount=transaction.amount,
            date=next_date,
            category=transaction.category,
            is_recurring=True,
            transaction_type=transaction.transaction_type,
            description=transaction.description
        ).exists()

        if not exists:
            Transaction.objects.create(
                user=transaction.user,
                amount=transaction.amount,
                date=next_date,
                category=transaction.category,
                is_recurring=True,
                transaction_type=transaction.transaction_type,
                description=transaction.description
            )

    def update(self, instance, data):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
