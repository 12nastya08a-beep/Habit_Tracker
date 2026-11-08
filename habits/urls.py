from django.urls import path
from .views import habit_detail, habit_list_create

urlpatterns = [
    path('habits/', habit_list_create, name='habit-list-create'),
    path('habits/<int:pk>/', habit_detail, name='habit-detail'),
]
