from django.urls import path, include

urlpatterns = [
    path('accounts/', include('expense_app.accounts.urls')), 
    path('expenses/', include('expense_app.expenses.urls')),
]
