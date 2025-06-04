from rest_framework.exceptions import ValidationError
from ..models import Category

class CategoryService:
    def __init__(self, user):
        self.user = user

    def create(self, data):
        if Category.objects.filter(user=self.user, name__iexact=data['name'], type=data['type']).exists():
            raise ValidationError(f"This {data['type']} category already exists.")
        return Category.objects.create(user=self.user, **data)

    def update(self, instance, data):
        if 'name' in data:
            if Category.objects.filter(user=self.user, name__iexact=data['name'], type=instance.type).exclude(id=instance.id).exists():
                raise ValidationError(f"This {instance.type} category already exists.")
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
