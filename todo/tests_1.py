import unittest
from .task_manager import TaskManager  # Import TaskManager from task_manager

class TestTaskManager(unittest.TestCase):
    
    def setUp(self):
        self.manager = TaskManager()

    def test_add_task(self):
        task = self.manager.add_task("Buy groceries", "2024-10-20", "High")
        
        # Assert that the task was added successfully
        self.assertEqual(len(self.manager.get_tasks()), 1)
        self.assertEqual(task.name, "Buy groceries")
        self.assertEqual(task.due_date, "2024-10-20")
        self.assertEqual(task.priority, "High")
        self.assertFalse(task.completed)

    def test_complete_task(self):
        task = self.manager.add_task("Finish homework", "2024-10-15", "Medium")
        task.complete_task()
        
        # Assert that the task was marked as complete
        self.assertTrue(task.completed)

if __name__ == '__main__':
    unittest.main()

#python -m unittest todo.tests_1 to run the test to do a unit test 
#kien test case scenario #1 