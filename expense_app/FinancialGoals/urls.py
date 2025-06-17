from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .view import SavingGoalViewSet

router = DefaultRouter()
router.register(r'saving-goals', SavingGoalViewSet, basename='savinggoal')

urlpatterns = [
    path('', include(router.urls)),
]
