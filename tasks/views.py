from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .tasks import send_email_async
from .pagination import TaskPagination
from .serializers import TaskSerializer

def index(request):
    return render(request, 'tasks/index.html')

class TaskListView(APIView):
    """List all tasks or create a new task"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.all()
        paginator = TaskPagination()
        paginated_tasks = paginator.paginate_queryset(tasks, request, view=self)
        serializer = TaskSerializer(paginated_tasks, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            send_email_async(task.email, task.title, "creada")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    """Retrieve, update or delete a task instance"""
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk)

    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            task = serializer.save()
            send_email_async(task.email, task.title, "actualizada")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response(
            {"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
