import logging

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Habit
from .serializers import HabitSerializer

logger = logging.getLogger(__name__)


@extend_schema(
    methods=["GET"],
    responses={200: HabitSerializer(many=True)},
)
@extend_schema(
    methods=["POST"],
    request=HabitSerializer,
    responses={201: HabitSerializer, 400: None},
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def habit_list_create(request):
    if request.method == "GET":
        habits = Habit.objects.all()
        serializer = HabitSerializer(habits, many=True)
        logger.info("Fetched habits list: count=%s", len(habits))
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = HabitSerializer(data=request.data)
    if serializer.is_valid():
        habit = serializer.save()
        logger.info("Created habit: id=%s, user_id=%s", habit.id, request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    logger.warning("Failed to create habit: invalid data")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=["GET"],
    responses={200: HabitSerializer, 404: None},
)
@extend_schema(
    methods=["PATCH"],
    request=HabitSerializer,
    responses={200: HabitSerializer, 400: None, 404: None},
)
@extend_schema(
    methods=["DELETE"],
    responses={204: None, 400: None, 404: None},
)
@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def habit_detail(request, pk):
    habit = get_object_or_404(Habit, pk=pk)

    if request.method == "GET":
        serializer = HabitSerializer(habit)
        logger.info("Fetched habit: id=%s", habit.id)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        serializer = HabitSerializer(habit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Updated habit: id=%s, user_id=%s", habit.id, request.user.id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning("Failed to update habit: id=%s, invalid data", habit.id)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if habit.logs.exists():
        logger.warning("Blocked habit deletion: id=%s has linked logs", habit.id)
        return Response(
            {
                "error": (
                    "Неможливо видалити звичку, оскільки до неї"
                    " прив'язані логи виконання."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    habit_id = habit.id
    habit.delete()
    logger.info("Deleted habit: id=%s, user_id=%s", habit_id, request.user.id)
    return Response(status=status.HTTP_204_NO_CONTENT)
