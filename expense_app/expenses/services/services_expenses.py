from ..models import Expense
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

from rest_framework.exceptions import ValidationError

class ExpenseService:
    def __init__(self, user):
        self.user = user

    def validate_limit(self, category, amount, date):
        if category.expense_limit is None:
            return
        total = Expense.objects.filter(
            user=self.user,
            category=category,
            date__year=date.year,
            date__month=date.month
        ).aggregate(Sum("amount"))['amount__sum'] or 0
        if total + amount > category.expense_limit:
            raise ValidationError(
                f"Sorry, adding the expense exceeded the upper limit for the category'{category.name}' ({category.expense_limit})."
            )

    def create(self, data):
        self.validate_limit(data['category'], data['amount'], data['date'])
        expense = Expense.objects.create(user=self.user, **data)
        if data.get("is_recurring"):
            Expense.objects.create(
                user=self.user,
                amount=data['amount'],
                date=data['date'] + relativedelta(months=1),
                category=data['category'],
                is_recurring=True,
                description=data.get('description', '')
            )
        return expense
    
