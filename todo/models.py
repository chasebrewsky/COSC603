from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class TodoList(models.Model):
    name = models.CharField(max_length=255, default='')
    user = models.ForeignKey(get_user_model(), models.CASCADE)


class Todo(models.Model):
    todo_list = models.ForeignKey(TodoList, models.CASCADE)
    description = models.TextField(default='')
    is_complete = models.BooleanField(default=False)

