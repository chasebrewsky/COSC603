from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase, Client
from todo.forms import SignupForm, TodoListForm, TodoForm, TodoBulkEditForm
from todo.models import Todo, TodoList
from todo.views import login, signup, home, view_list, create_list, create_todo, edit_todo


class TestSignupForm(TestCase):
    """Tests for the signup form."""
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='user', email='user@email.com',
        )
        self.todo_list = TodoList.objects.create(
            name='list', user=self.user,
        )
        self.todo = Todo.objects.create(
            todo_list=self.todo_list,
            description='Something'
        )

    def test_username_exists(self):
        """Form should not be valid if existing username."""
        data = {
            'username': 'user',
            'email': 'another@email.com',
            'password': 'password',
            'password_repeated': 'password',
        }
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEquals({
            'username': ['User with username already exists'],
        }, form.errors)

    def test_username_available(self):
        """Form should valid if username is available."""
        data = {
            'username': 'user5',
            'email': 'another5@email.com',
            'password': 'password',
            'password_repeated': 'password',
        }
        form = SignupForm(data=data)
        self.assertTrue(form.is_valid())

    def test_email_exists(self):
        """Form should not be valid if existing email."""
        data = {
            'username': 'test',
            'email': 'user@email.com',
            'password': 'password',
            'password_repeated': 'password',
        }
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEquals({
            'email': ['User with email already exists'],
        }, form.errors)

    def test_email_available(self):
        """Form should valid if existing email."""
        data = {
            'username': 'test4',
            'email': 'user@gmail.com',
            'password': 'password',
            'password_repeated': 'password',
        }
        form = SignupForm(data=data)
        self.assertTrue(form.is_valid())

    def test_password_matches(self):
        """Form should not be valid if passwords don't match"""
        data = {
            'username': 'user2',
            'email': 'another2@email.com',
            'password': 'password2',
            'password_repeated': 'password3',
        }
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEquals({
            '__all__': ['Passwords do not match']
        }, form.errors)

    def test_password_valid(self):
        """Form should be valid if passwords match."""
        data = {
            'username': 'test6',
            'email': 'user6@gmail.com',
            'password': 'password',
            'password_repeated': 'password',
        }
        form = SignupForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_valid_data(self):
        """Test for all fields valid"""
        form = SignupForm(data={
            'username': 'test7',
            'email': 'test7@email.com',
            'password': 'password7',
            'password_repeated': 'password7'
        })
        self.assertTrue(form.is_valid())


class TestTodoListForm(TestCase):
    """Tests for the todo list form."""
    def setUp(self):
        self.user = get_user_model().objects.create(
             username='user', email='user@email.com',
        )

    def test_todo_list_requires_user(self):
        """Lists require a user to be assigned to them."""
        data = {'name': 'Test'}
        form = TodoListForm(data=data)
        self.assertRaises(IntegrityError, lambda: form.save())

    def test_todo_list_made(self):
        """Lists with a user assigned to them should pass."""
        data = {'name': 'Test'}
        form = TodoListForm(data=data)
        todo_list = form.save(commit=False)
        todo_list.user = self.user
        todo_list.save()
        self.assertEquals(todo_list.name, 'Test')


class TestTodoForm(TestCase):
    """Tests for the todo form."""
    def setUp(self):
        self.user = get_user_model().objects.create(
             username='user', email='user@email.com',
        )

class TestTodoBulkEditForm(TestCase):
    """Test for Todo Bulk Edit Form."""
    def setUp(self):
        self.user = get_user_model().objects.create(
             username='user', email='user@email.com',
        )

class TodoTests(TestCase):
    def test_string_representation(self):
        entry = TodoList(name="My entry name")
        self.assertEqual(str(entry), entry.name)

    def test_description_is_greater_than_1(self):
        """
        Check if the size of the string is more than 1
        Return true if it meets the size requirements
        """
        description_string = Todo(description="Checking the size")
        self.assertEqual(description_string.description_is_more_than_0(), True)

    def test_string_representation_todo(self):
        entry = Todo(description="My description name")
        self.assertEqual(str(entry), entry.description)


    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 301)

    def test_logout(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 301)

    def test_signup(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 301)

    def test_lists_create(self):
        response = self.client.get('/lists/create')
        self.assertEqual(response.status_code, 301)

    def test_admin(self):
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 301)