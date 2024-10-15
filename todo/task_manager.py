class Task:
    def __init__(self, name, due_date, priority):
        # Initialize a new Task with name, due date, and priority
        self.name = name
        self.due_date = due_date
        self.priority = priority
        # By default, the task is not completed
        self.completed = False

    def complete_task(self):
        # Method to mark the task as completed
        self.completed = True

    def __repr__(self):
        # Representation of the task for debugging purposes
        return f"Task({self.name}, Due: {self.due_date}, Priority: {self.priority}, Completed: {self.completed})"

class TaskManager:
    def __init__(self):
        # Initialize the task manager with an empty list of tasks
        self.tasks = []

    def add_task(self, name, due_date, priority):
        # Create a new Task and add it to the task list
        task = Task(name, due_date, priority)
        self.tasks.append(task)  # Add the new task to the list
        return task  # Return the created task

    def get_tasks(self):
        # Return the list of tasks
        return self.tasks
