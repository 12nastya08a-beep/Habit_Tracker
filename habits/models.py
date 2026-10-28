from django.contrib.auth.models import User
from django.db import models

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits', blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        status = 'Виконано' if self.is_completed else 'Не виконано'
        return f'{self.habit.title} - {self.date} ({status})'
