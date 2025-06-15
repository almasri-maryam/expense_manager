from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate-monthly-recurring-transactions': {
        'task': 'expense_app.expenses.tasks.generate_monthly_recurring_transactions',
        'schedule': crontab(minute=0, hour=0, day_of_month=1),  
    },
}


#celery -A core beat --loglevel=info           
# celery -A core  worker --loglevel=info 
