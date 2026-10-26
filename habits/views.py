from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Habit
from .serializers import HabitSerializer


@api_view(['GET', 'POST'])
def habit_list_create(request):
    """Отримати список усіх звичок або створити нову"""
    if request.method == 'GET':
        habits = Habit.objects.all()
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = HabitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PATCH', 'DELETE'])
def habit_detail(request, pk):
    """Отримати, оновити або видалити конкретну звичку за її ID"""
    habit = get_object_or_404(Habit, pk=pk)

    if request.method == 'GET':
        serializer = HabitSerializer(habit)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        serializer = HabitSerializer(habit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if habit.logs.exists():
            return Response(
                {
                    "error": (
                        "Неможливо видалити звичку, оскільки до неї"
                        " прив'язані логи виконання."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        habit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
