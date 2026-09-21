from _testcapi import MethInstance
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models



USER_STATUS = (
    ('beginner', 'beginner'),
    ('active', 'active'),
    ('pro', 'pro')
)


class UserProfile(AbstractUser):
    age = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(70)], null=True, blank=True)
    phone_number = PhoneNumberField(default='+996')
    avatar = models.ImageField(upload_to='UserImage', null=True, blank=True)
    status = models.CharField(max_length=10, choises=USER_STATUS, default='beginner')
    data_register = models.DateField(auto_now_add=True)


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    category_img = models.ImageField(upload_to='UserImage', null=True, blank=True)


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects')
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='owner')
    created_at = models.DateTimeField(auto_now_add=True)


    def get_tasks_count(self):
        return self.tasks.count()

    def get_completed_percent(self):
        total = self.tasks.count()

        if total == 0:
            return 0

        completed = self.tasks.filter(status='completed').count()

        return (completed / total) * 100


class Tag(models.Model):
    tag_name = models.CharField(30, unique=True)


