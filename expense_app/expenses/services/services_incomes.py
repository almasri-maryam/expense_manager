from ..models import Income

class IncomeService:
    def __init__(self, user):
        self.user = user

    def create(self, data):
        return Income.objects.create(user=self.user, **data)

    def update(self, instance, data):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
