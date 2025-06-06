from user.models import BaseModel, CustomUser
from django.db import models

class FitnessClass(BaseModel):
    COMPONENT_CHOICES = [
        ('Yoga', 'Yoga'),
        ('Zumba', 'Zumba'),
        ('HIIT', 'HIIT'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes")  
    type = models.CharField(max_length=10, choices=COMPONENT_CHOICES)
    instructor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': CustomUser.Roles.INSTRUCTOR},
        related_name='fitness_classes'
    )

    def __str__(self):
        return f"{self.name} on {self.date} at {self.time}"


class Booking(BaseModel):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')

    def __str__(self):
        return f"{self.user} booked {self.fitness_class}"
