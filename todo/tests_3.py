from django.test import TestCase
from .models import Task 

#Example test case for editing a task
class EditTaskTestCase(TestCase):
    def setUp(self):
        # This method runs before each test
        Task.objects.create(name="NewTask", due_date="2024-10-15", priority="High")

    def test_edit_task(self):
        """Test editing a task's due date and priority"""
        # User navigates to the task list on the home screen (simulated by setup)
        # User clicks the Edit button next to the task and changes the due date or priority
        self.task.due_date = "2024-12-01"
        self.task.priority = "Medium"
        self.task.save()

        # Fetch the updated task
        updated_task = Task.objects.get(id=self.task.id)

        # Verify the changes
        self.assertEqual(updated_task.due_date, "2024-12-01")
        self.assertEqual(updated_task.priority, "Medium")

