from django.test import TestCase
from .models import Task  # Make sure this matches the name of your model for tasks

# Example test case for adding a task
class TaskTestCase(TestCase):
    def setUp(self):
        # This method runs before each test
        Task.objects.create(name="Initial Task", due_date="2024-10-15", priority="High")

    def test_add_task(self):
        """Test adding a new task"""
        task = Task.objects.create(name="New Task", due_date="2024-10-20", priority="Medium")
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(task.name, "New Task")
        self.assertEqual(task.priority, "Medium")

# Example test case for marking a task as completed
class CompleteTaskTestCase(TestCase):
    def setUp(self):
        # Setup code that runs before each test
        self.task = Task.objects.create(name="Incomplete Task", due_date="2024-12-01", completed=False)

    def test_complete_task(self):
        """Test completing a task"""
        self.task.completed = True
        self.task.save()
        completed_task = Task.objects.get(name="Incomplete Task")
        self.assertTrue(completed_task.completed)
        
    #bhumik test case scenario #2