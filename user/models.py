import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager



class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
class CustomUserManager(BaseUserManager):


    def create_user(self,username,name, email, password, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        if not email:
            raise ValueError("The email must be set")
        if not name:
            raise ValueError("The name must be set")
        
        user = self.model(
            username=username,
            name=name,
            email=email,
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



    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']  

    objects = CustomUserManager()

    def __str__(self):
        return self.username

