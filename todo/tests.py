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

# class TestSignupForm(TestCase):
#     """Tests for the signup form."""
#
#     def setUp(self):
#         self.user = get_user_model().objects.create(
#             username='user', email='user@email.com',
#         )
#         self.todo_list = TodoList.objects.create(
#             name='list', user=self.user,
#         )
#         self.todo = Todo.objects.create(
#             todo_list=self.todo_list,
#             description='Something'
#         )
#
#     def test_username_exists(self):
#         """Form should not be valid if existing username."""
#         data = {
#             'username': 'user',
#             'email': 'another@email.com',
#             'password': 'password',
#             'password_repeated': 'password',
#         }
#         form = SignupForm(data=data)
#         self.assertFalse(form.is_valid())
#         self.assertEquals({
#             'username': ['User with username already exists'],
#         }, form.errors)
#
#     def test_email_exists(self):
#         """Form should not be valid if existing email."""
#         data = {
#             'username': 'test',
#             'email': 'user@email.com',
#             'password': 'password',
#             'password_repeated': 'password',
#         }
#         form = SignupForm(data=data)
#         self.assertFalse(form.is_valid())
#         self.assertEquals({
#             'email': ['User with email already exists'],
#         }, form.errors)
#
#
# class TestTodoListForm(TestCase):
#     """Tests for the todo list form."""
#     def setUp(self):
#         self.user = get_user_model().objects.create(
#             username='user', email='user@email.com',
#         )
#
#     def test_todo_list_requires_user(self):
#         """Lists require a user to be assigned to them."""
#         data = {'name': 'Test'}
#         form = TodoListForm(data=data)
#         self.assertRaises(IntegrityError, lambda: form.save())
#
#     def test_todo_list_made(self):
#         """Lists with a user assigned to them should pass."""
#         data = {'name': 'Test'}
#         form = TodoListForm(data=data)
#         todo_list = form.save(commit=False)
#         todo_list.user = self.user
#         todo_list.save()
#         self.assertEquals(todo_list.name, 'Test')
