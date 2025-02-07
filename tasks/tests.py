from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

User = get_user_model()


class TaskAPITestCase(APITestCase):
    """Test cases for Task API"""

    def setUp(self):
        """Create test user and sample tasks"""
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.task1 = Task.objects.create(
            title="Task 1",
            email="task1@example.com",
            description="Description 1",
        )
        self.task2 = Task.objects.create(
            title="Task 2",
            email="task2@example.com",
            description="Description 2",
        )
        self.task_list_url = reverse("task-list")
        self.task_detail_url = lambda pk: reverse("task-detail", kwargs={"pk": pk})

    def test_list_tasks(self):
        """Test a list of tasks"""
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 2)

    def test_create_task(self):
        """Test creating a new task"""
        data = {
            "title": "New Task",
            "email": "newtask@example.com",
            "description": "New Description",
        }
        response = self.client.post(self.task_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    def test_update_task(self):
        """Test updating an existing task"""
        data = {"title": "Updated Task", "description": "Updated Description"}
        response = self.client.put(
            self.task_detail_url(self.task1.pk), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, "Updated Task")
        self.assertEqual(self.task1.description, "Updated Description")

    def test_delete_task(self):
        """Test deleting a task"""
        response = self.client.delete(self.task_detail_url(self.task1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access the API"""
        self.client.logout()
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
