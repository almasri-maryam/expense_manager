from expense_app.expenses.models import Transaction
from django.db.models import Sum
from collections import defaultdict
from datetime import timedelta, datetime
from django.utils.timezone import now
from calendar import month_name

class DashboardService:
    def __init__(self, user):
        self.user = user

    def get_total(self, transaction_type):
        return (
            Transaction.objects
            .filter(user=self.user, transaction_type=transaction_type)
            .aggregate(total=Sum('amount'))['total'] or 0
        )

    def get_total_expenses(self):
        return self.get_total(Transaction.EXPENSE)

    def get_total_incomes(self):
        return self.get_total(Transaction.INCOME)

    def get_expenses_by_category(self):
        queryset = (
            Transaction.objects
            .filter(user=self.user, transaction_type=Transaction.EXPENSE)
            .values('category__name')
            .annotate(total=Sum('amount'))
        )
        return {entry['category__name']: entry['total'] for entry in queryset}

    def get_incomes_by_category(self):
        queryset = (
            Transaction.objects
            .filter(user=self.user, transaction_type=Transaction.INCOME)
            .values('category__name')
            .annotate(total=Sum('amount'))
        )
        return {entry['category__name']: entry['total'] for entry in queryset}

    def get_expense_trend_by_date(self):
        queryset = (
            Transaction.objects
            .filter(user=self.user, transaction_type=Transaction.EXPENSE)
            .values('date', 'category__name')
            .annotate(total=Sum('amount'))
        )
        result = defaultdict(lambda: defaultdict(float))
        for entry in queryset:
            result[str(entry['date'])][entry['category__name']] = float(entry['total'])
        return result

    def get_income_trend_by_date(self):
        queryset = (
            Transaction.objects
            .filter(user=self.user, transaction_type=Transaction.INCOME)
            .values('date', 'category__name')
            .annotate(total=Sum('amount'))
        )
        result = defaultdict(lambda: defaultdict(float))
        for entry in queryset:
            result[str(entry['date'])][entry['category__name']] = float(entry['total'])
        return result

    def get_dashboard_data(self):
        return {
            "total_expenses": self.get_total_expenses(),
            "total_incomes": self.get_total_incomes(),
            "expenses_by_category": self.get_expenses_by_category(),
            "incomes_by_category": self.get_incomes_by_category(),
            "expense_trend": self.get_expense_trend_by_date(),
            "income_trend": self.get_income_trend_by_date(),
        }
