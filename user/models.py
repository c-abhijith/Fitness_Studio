import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import pytz



class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
        
class CustomUserManager(BaseUserManager):

    def validate_required_fields(self, **fields):
        for field_name, value in fields.items():
            if not value:
                raise ValueError(f"The {field_name} must be set")

    def create_user(self, username, name, email, password, timezone_str, **extra_fields):
        self.validate_required_fields(
            username=username,
            name=name,
            email=email,
            timezone=timezone_str
        )

        user = self.model(
            username=username,
            name=name,
            email=email,
            timezone=timezone_str,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    
class CustomUser(BaseModel,AbstractUser):
    class Roles(models.TextChoices):
        INSTRUCTOR = "instructor", "Instructor"
        USER = "user", "User"

    username = models.CharField(max_length=150, unique=True)  
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER)
    timezone = models.CharField(max_length=50, choices=[(tz, tz) for tz in pytz.common_timezones], default='UTC')



    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']  

    objects = CustomUserManager()

    def __str__(self):
        return self.username

