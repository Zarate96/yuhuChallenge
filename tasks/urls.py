from django.urls import path
from .views import TaskListView, TaskDetailView, index
urlpatterns = [
    path('home/', index, name='index'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
