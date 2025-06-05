from django.db import models
from user.models import BaseModel,CustomUser
from django.core.exceptions import ValidationError



class WorkingHour(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    weekly_schedule = models.JSONField()

    def clean(self):
        if self.user.role != CustomUser.Roles.INSTRUCTOR:
            raise ValidationError("Working hours can only be assigned to instructors.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.name}'s Working Hours"
