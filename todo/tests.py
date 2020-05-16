from django.test import TestCase

from .models import Todo, TodoList

class TodoTests(TestCase):
    def test_is_not_empty(self):
        """
        Check if this name is Empty
        Return true if not empty
        """
        entryName = TodoList(name="Some name")
        self.assertIs(entryName.is_not_empty(), True)

    def test_is_not_null(self):
        """
        Check if name is null
        Return True if it not null
        """
        entryName = TodoList(name="Some name")
        self.assertEqual(entryName.is_not_null(), True)

    def test_is_less_than_255(self):
        """
        Check if the size of the string is less than 255
        Return true if it meets the size requirements
        """
        entryName = TodoList(name="Checking the size")
        self.assertEqual(entryName.is_less_than_255(), True)

    def test_string_representation(self):
        entry = TodoList(name="My entry name")
        self.assertEqual(str(entry), entry.name)

    def test_description_is_not_empty(self):
        """
        Check if this name is Empty
        Return true if not empty
        """
        descstring = Todo(description="Some description")
        self.assertIs(descstring.description_is_not_empty(), True)

    def test_description_is_not_null(self):
        """
        Check if name is null
        Return True if it not null
        """
        descstring = Todo(description="Some description")
        self.assertEqual(descstring.description_is_not_null(), True)

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