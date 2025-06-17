from rest_framework import serializers
from .models import SavingGoal

class SavingGoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SavingGoal
        fields = [
            'id', 'title', 'target_amount', 'current_amount',
            'progress_percentage', 'deadline', 'is_achieved',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['is_achieved', 'created_at', 'updated_at', 'progress_percentage']

    def get_progress_percentage(self, obj):
        if obj.target_amount == 0:
            return 0
        percentage = (obj.current_amount / obj.target_amount) * 100
        return round(min(percentage, 100), 1)
