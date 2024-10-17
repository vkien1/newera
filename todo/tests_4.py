from django.test import TestCase
from .models import Task

# Example test case for deleting a task
class DeleteTaskTestCase(TestCase):
    def setUp(self):
        # This method runs before each test
        Task.objects.create(name="New Task", due_date="2024-10-15", priority="High")

    def test_delete_task(self):
        self.assertEqual(Task.objects.count(), 1)
        # TODO delete new task
        self.assertEqual(Task.objects.count(), 0)
        
#june test case scenario #4