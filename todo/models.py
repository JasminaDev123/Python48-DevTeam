from _testcapi import MethInstance
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.utils import timezone



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


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium",)
    deadline = models.DateTimeField(null=True, blank=True,)
    created_date = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey("Project", related_name="tasks", on_delete=models.CASCADE,)
    assignee = models.ForeignKey("UserProfile", null=True, blank=True, on_delete=models.SET_NULL,)
    tags = models.ManyToManyField("Tag", blank=True,)

    def get_progress(self):
        total = self.subtasks.count()

        if total == 0:
            return 0

        completed = self.subtasks.filter(completed=True).count()

        return int(completed / total * 100)

    def get_comments_count(self):
        return self.comments.count()

    def is_overdue(self):
        if self.completed:
            return False

        if self.deadline is None:
            return False

        return timezone.now() > self.deadline

    def __str__(self):
        return self.title


class Subtask(models.Model):
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TaskFile(models.Model):
    task = models.ForeignKey(Task, related_name='files', on_delete=models.CASCADE)
    image = models.FileField(upload_to='task_files/')


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, related_name="favorite", on_delete=models.CASCADE)

class FavoriteItem(models.Model):
    Favorite = models.ForeignKey(Favorite, related_name="items", on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)