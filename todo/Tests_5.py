import unittest 
class MockTask:
    """A simple mock task class for testing purposes."""
    def __init__(self, title, status):
        self.title = title
        self.status = status

class ToDoListFilterTest(unittest.TestCase):

    def setUp(self):
        # Simulate tasks using MockTask
        self.tasks = [
            MockTask(title="Task 1", status="pending"),
            MockTask(title="Task 2", status="completed"),
            MockTask(title="Task 3", status="completed")
        ]

    def mock_get_tasks(self, status=None):
        """A mock function to simulate task retrieval."""
        if status == "completed":
            return [task for task in self.tasks if task.status == "completed"]
        elif status == "pending":
            return [task for task in self.tasks if task.status == "pending"]
        return self.tasks

    def test_view_all_tasks(self):
        # Simulate viewing all tasks
        all_tasks = self.mock_get_tasks()
        self.assertEqual(len(all_tasks), 3)  # Check if all tasks are returned

        # Check that all tasks are in the list
        for task in self.tasks:
            self.assertIn(task.title, [t.title for t in all_tasks])

    def test_filter_completed_tasks(self):
        # Simulate filtering completed tasks
        completed_tasks = self.mock_get_tasks(status="completed")
        self.assertEqual(len(completed_tasks), 2)  # Check that only completed tasks are returned

        # Check that only completed tasks are in the list
        for task in completed_tasks:
            self.assertEqual(task.status, "completed")

    def test_filter_pending_tasks(self):
        # Simulate filtering pending tasks
        pending_tasks = self.mock_get_tasks(status="pending")
        self.assertEqual(len(pending_tasks), 1)  # Check that only pending tasks are returned

        # Check that only pending tasks are in the list
        for task in pending_tasks:
            self.assertEqual(task.status, "pending")

if __name__ == '__main__':
    unittest.main()