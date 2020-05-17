from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class TodoList(models.Model):
    name = models.CharField(max_length=255, default='')
    user = models.ForeignKey(get_user_model(), models.CASCADE)

    def __str__(self):
        return self.name

    def is_not_empty(self):
        namentry = self.name
        if namentry == "":
            return False
        else:
            return True

    def is_not_null(self):
        namentry = self.name
        if not namentry:
            return False
        else:
            return True

    def is_less_than_255(self):
        if(len(self.name)<255):
            return True
        else:
            return False


class Todo(models.Model):
    todo_list = models.ForeignKey(TodoList, models.CASCADE)
    description = models.TextField(default='')
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.description

    def description_is_not_empty(self):
        descriptionstring = self.description
        if descriptionstring == "":
            return False
        else:
            return True

    def description_is_not_null(self):
        descriptionstring = self.description
        if not descriptionstring:
            return False
        else:
            return True

    def description_is_more_than_0(self):
        if(len(self.description)>0):
            return True
        else:
            return False
