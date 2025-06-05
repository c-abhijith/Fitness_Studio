from user.models import BaseModel, CustomUser
from django.db import models

class FitnessClass(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes")  
    max_members = models.PositiveIntegerField(default=20)
    instructor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': CustomUser.Roles.INSTRUCTOR},
        related_name='fitness_classes'
    )

    def __str__(self):
        return f"{self.name} on {self.date} at {self.time}"
