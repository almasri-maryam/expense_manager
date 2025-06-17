from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SavingGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saving_goals')
    title = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField(null=True, blank=True)
    is_achieved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # تحديث حالة الإنجاز تلقائيًا
        self.is_achieved = self.current_amount >= self.target_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.current_amount}/{self.target_amount})"
