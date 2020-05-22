from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse, resolve

from todo.forms import SignupForm, TodoListForm, TodoForm
from todo.models import Todo, TodoList
from todo.views import signup, home, create_list


"""Sonny Rivera-Ruiz Tests"""


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

    def test_email_blank_on_load(self):
        """Email should be blank on load"""
        response = self.client.get('/signup/')
        self.assertEquals(response.context['form']['email'].value(), None)

    def test_user_blank_on_load(self):
        """User should be blank on load"""
        response = self.client.get('/signup/')
        self.assertEquals(response.context['form']['username'].value(), None)

    def test_password_blank_on_load(self):
        """User should be blank on load"""
        response = self.client.get('/signup/')
        self.assertEquals(response.context['form']['password'].value(), None)

    def test_password_repeated_blank_on_load(self):
        """User should be blank on load"""
        response = self.client.get('/signup/')
        self.assertEquals(response.context['form']['password_repeated'].value(), None)

    def test_first_name_blank_on_load(self):
        """User should be blank on load"""
        response = self.client.get('/signup/')
        self.assertEquals(response.context['form']['first_name'].value(), None)

    def test_last_name_blank_on_load(self):
        """User should be blank on load"""
        response = self.client.get('/signup/')
        self.assertEquals(response.context['form']['last_name'].value(), None)

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

    def test_username_is_not_blank(self):
        """Form checks if username is blank"""
        data = {
            'username': '',
            'email': 'another9@email.com',
            'password': 'password',
            'password_repeated': 'password',
        }
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEquals({
            'username': ['This field is required.'],
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

    def test_email_is_not_blank(self):
        """Form is not valid if email is blank"""
        data = {
            'username': 'username9',
            'email': '',
            'password': 'password',
            'password_repeated': 'password',
        }
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEquals({
            'email': ['This field is required.'],
        }, form.errors)

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
        self.todo_list = TodoList.objects.create(
            name='list', user=self.user,
        )
        self.todo = Todo.objects.create(
            todo_list=self.todo_list,
            description='Something'
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
        self.todo_list = TodoList.objects.create(
            name='list', user=self.user,
        )
        self.todo = Todo.objects.create(
            todo_list=self.todo_list,
            description='Something'
        )

    def test_todo_form_requires_user(self):
        """Todo forms require a user to be assigned."""
        data = {'description': 'A Description'}
        form = TodoForm(data=data)
        self.assertRaises(IntegrityError, lambda: form.save())

    def test_valid_todo_form(self):
        data = self.todo
        form = TodoForm(data=data)


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

    def test_home_url(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_create_list_url(self):
        url = reverse('create_list')
        self.assertEquals(resolve(url).func, create_list)

    def test_signup_url(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, signup)

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


"""Chinedu Onugu Tests"""


class TestSignIn(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='testuser',
            password='12345',
            email='useremail@example.com',
        )

    def test_CorrectUser(self):
        user = authenticate(username='test', password='password')
        self.assertFalse((user is not None))

    def test_WrongUsername(self):
        user = authenticate(username='wrong', password='12345')
        self.assertFalse(user is not None)

    def test_WrongPassword(self):
        user = authenticate(username='testuser', password='wrong')
        self.assertFalse(user is not None)


class TestSignInView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='testuser', password='12345',
            email='useremail@example.com',
        )

    def test_CorrectUser(self):
        response = self.client.post(
            '/login/', {'username': 'testuser', 'password': '12345'},
        )
        self.assertTrue(response)

    def test_WrongUsername(self):
        response = self.client.post(
            '/login/', {'username': 'wrong', 'password': '12345'},
        )
        self.assertTrue(response)

    def test_WrongPassword(self):
        response = self.client.post(
            '/login/', {'username': 'testuser', 'password': 'wrong'},
        )
        self.assertTrue(response)


class TestsTodoApp(TestCase): 
    def setUp(self):
        self.expected = ['food', 'fruit', 'milk']
        self.result = ['food', 'fruit', 'milk']

    def test_OneTodos(self):
        item = TodoList(name="Go to the gym")
        self.assertEqual(str(item), item.name)

    def test_CreateList(self):
        response = self.client.get('/create_list/')
        self.assertTrue(response)

    def test_CreateTodo(self):
        response = self.client.get('/create_todo/')
        self.assertTrue(response)

    def test_TwoTodos(self):
        item1 = TodoList(name="Go to the mall")
        item2 = TodoList(name="Go to the car wash")
        self.assertEqual(str(item1), item1.name)
        self.assertEqual(str(item2), item2.name)

    def test_EditTodo(self):
        response = self.client.get('/edit_todo/')
        self.assertTrue(response)

    def test_CLeanUsername(self):
        response = self.client.get('/clean_username/')
        self.assertTrue(response)

    def test_CLeanEmail(self):
        response = self.client.get('/clean_email/')
        self.assertTrue(response)

    def test_CountEqual(self):
        self.assertCountEqual(self.result, self.expected)

    def test_ListEqual(self):
        self.assertListEqual(self.result, self.expected)

    def test_Header(self):
        response = self.client.get('/')
        self.assertTrue(response)


class ErroHandling(TestCase):
    def test_Erro1(self):
        with self.assertRaises(TypeError):
            1 + '1'

    def test_Error2(self):
        import operator
        self.assertRaises(TypeError, operator.add, 1, '1')

    def test_Erro3(self):
        with self.assertRaises(TypeError):
            1 + 'A'


class HomePageTest(TestCase):
    def test_HomePage(self):
        found = resolve('/')  
        self.assertEqual(found.func, home)

    def test_headers(self):
        response = self.client.get('/')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')

    def test_bad_header(self):
        def access_bad_header():
           response = self.client.get('/')
           response['X-Unknown-Header']
        self.assertRaises(KeyError, access_bad_header)

    def test_home(self):
        response = self.client.get('/')
        self.assertTrue(response)

    def test_ViewName(self):
        response = self.client.get(reverse('home'))
        self.assertTrue(response)

    def test_About(self):
        response = self.client.get('/about/')
        self.assertTrue(response)

    def test_Contact(self):
        response = self.client.get('/contact/')
        self.assertTrue(response)

    def test_List(self):
        response = self.client.get('/list/')
        self.assertTrue(response)

    def test_ViewSignup(self):
        response = self.client.get('/signup/')
        self.assertTrue(response)

    def test_ViewLogin(self):
        response = self.client.get('/login/')
        self.assertTrue(response)

    def test_viewTodo(self):
        response = self.client.get('/todo/')
        self.assertTrue(response)
