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
    category_name = models.CharField()
