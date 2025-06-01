
from django.db import models
from django.contrib.auth import get_user_model


#User fetched
User = get_user_model()

#Expense and ExpenseCategory 
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    expense_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Expense(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
   # category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_recurring = models.BooleanField(default=False)
    description = models.TextField(blank=True)


# income and incomeCategory
class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Income(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=200)
    #category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True) 



