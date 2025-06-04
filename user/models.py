import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractUser):
    class Roles(models.TextChoices):
        INSTRUCTOR = "instructor", "Instructor"
        USER = "user", "User"

    username = models.CharField(max_length=150, unique=True)  
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']  
    def __str__(self):
        return self.username


class WorkingHour(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weekly_schedule = models.JSONField()

    def clean(self):
        if self.user.role != User.Roles.INSTRUCTOR:
            raise ValidationError("Working hours can only be assigned to instructors.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.name}'s Working Hours"
