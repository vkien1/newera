from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=255)
    due_date = models.DateField()
    priority = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

