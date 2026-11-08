from rest_framework import serializers
from .models import Habit, HabitLog


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ['id', 'habit', 'date', 'is_completed']


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'user', 'title', 'description', 'created_at']
        read_only_fields = ['user', 'created_at']
