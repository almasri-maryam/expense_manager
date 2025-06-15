# expense_app/expenses/tasks.py
from celery import shared_task
from .models import Transaction
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now

@shared_task
def generate_monthly_recurring_transactions():
    today = now().date()
    last_month = today - relativedelta(months=1)

    recurring_transactions = Transaction.objects.filter(
        is_recurring=True,
        date__year=last_month.year,
        date__month=last_month.month
    )

    to_create = []
    for transaction in recurring_transactions:
        next_month = transaction.date + relativedelta(months=1)

        exists = Transaction.objects.filter(
            user=transaction.user,
            amount=transaction.amount,
            date=next_month,
            category=transaction.category,
            is_recurring=True,
            transaction_type=transaction.transaction_type,
            description=transaction.description
        ).exists()

        if not exists:
            to_create.append(Transaction(
                user=transaction.user,
                amount=transaction.amount,
                date=next_month,
                category=transaction.category,
                is_recurring=True,
                transaction_type=transaction.transaction_type,
                description=transaction.description
            ))

    if to_create:
        Transaction.objects.bulk_create(to_create)
