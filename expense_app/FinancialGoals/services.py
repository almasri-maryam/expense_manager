# services/goals.py
from .models import SavingGoal
from django.utils import timezone

class SavingGoalService:

    @staticmethod
    def create_goal(user, data):
        goal = SavingGoal.objects.create(user=user, **data)
        return goal

    @staticmethod
    def update_goal_progress(goal: SavingGoal, amount: float):
        goal.current_amount += amount
        goal.check_achieved()
        goal.save()
        return goal

    @staticmethod
    def get_user_goals(user):
        return SavingGoal.objects.filter(user=user)

    @staticmethod
    def delete_goal(goal_id, user):
        goal = SavingGoal.objects.get(id=goal_id, user=user)
        goal.delete()
