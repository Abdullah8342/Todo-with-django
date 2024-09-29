from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    STATUS_CHOICES = (
        ('Pending','Pending'),
        ('In progress','In progress'),
        ('Done','Done'),
    )
    todo_status = models.CharField(max_length=15,choices = STATUS_CHOICES)
    pub_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.title
