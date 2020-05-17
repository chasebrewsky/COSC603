from django.test import TestCase

from .models import Todo, TodoList

class TodoTests(TestCase):

    def test_string_representation(self):
        entry = TodoList(name="My entry name")
        self.assertEqual(str(entry), entry.name)

    def test_description_is_greater_than_1(self):
        """
        Check if the size of the string is more than 1
        Return true if it meets the size requirements
        """
        descstring = Todo(description="Checking the size")
        self.assertEqual(descstring.description_is_more_than_0(), True)

    def test_string_representation_todo(self):
        entry = Todo(description="My description name")
        self.assertEqual(str(entry), entry.description)

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)