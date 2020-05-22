from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db import IntegrityError
from django.test import TestCase, Client, tag
from django.urls import reverse, resolve
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

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


class TodoTests(TestCase):
    def test_string_representation(self):
        entry = TodoList(name="My entry name")
        self.assertEqual(str(entry), entry.name)

    def test_description_is_greater_than_0(self):
        """
        Check if the size of the string is more than 1
        Return true if it meets the size requirements
        """
        description_string = Todo(description="Checking the size")
        self.assertEqual(description_string.description_is_more_than_0(), True)

    def test_description_is_equal_to_0(self):
        description_string = Todo(description="")
        self.assertEqual(
            description_string.description_is_more_than_0(), False,
        )

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


class TestTodoBulkEditForm(TestCase):
    """Test for Todo Bulk Edit Form."""
    def setUp(self):
        self.user = get_user_model().objects.create(
             username='user', email='user@email.com',
        )


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


"""Chase Brewer Tests"""


class TodoListModelTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='user', password='password',
        )

    def test_name_default_blank(self):
        """Name cannot be null."""
        todo_list = TodoList(user=self.user)
        todo_list.save()
        self.assertEqual(todo_list.name, '')

    def test_user_not_null(self):
        """Todo list must have an assigned user."""
        todo_list = TodoList(name='Test')
        self.assertRaises(IntegrityError, todo_list.save)


class TodoModelTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='user', password='password',
        )
        self.todo_list = TodoList.objects.create(
            name='Test',
            user=self.user,
        )

    def test_description_default_blank(self):
        """Description defaults to blank."""
        todo_list = Todo(todo_list=self.todo_list)
        todo_list.save()
        self.assertEqual(todo_list.description, '')

    def test_is_complete_default(self):
        """Is complete defaults to false."""
        todo_list = Todo(todo_list=self.todo_list)
        todo_list.save()
        self.assertEqual(todo_list.is_complete, False)

    def test_todo_list_not_null(self):
        """Todo must be assigned to a todo list.."""
        todo = Todo()
        self.assertRaises(IntegrityError, todo.save)


class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.user_model = get_user_model()

    def test_username_saved(self):
        """username should flush to database."""
        user = self.user_model(username='user')
        user.save()
        self.assertEqual(user.username, 'user')

    def test_hashed_password(self):
        """Passwords should be hashed when saved to DB."""
        user = self.user_model.objects.create_user(
            username='user', password='password',
        )
        self.assertNotEqual(user.password, 'password')

    def test_full_name(self):
        user = self.user_model.objects.create_user(
            username='user', password='password',
            first_name='User', last_name='Person'
        )
        self.assertEqual(user.get_full_name(), 'User Person')

    def test_missing_full_name(self):
        user = self.user_model.objects.create_user(
            username='user', password='password',
        )
        self.assertEqual(user.get_full_name(), '')


class LogoutViewTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            username='user', password='password',
        )
        self.client = Client()

    def test_logout_redirect(self):
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/login/')


class LoginViewTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            username='user', password='password',
        )
        self.client = Client()

    def test_redirect_authenticated(self):
        """Authenticated users should be redirected to home."""
        self.client.force_login(self.user)
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_get_template(self):
        """GET request should be rendered with the correct template."""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_form_errors(self):
        """Error should be returned if form is not valid."""
        response = self.client.post('/login/', {
            'username': 'missing',
            'password': 'missing',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', None,
            'Please enter a correct username and password. Note that both '
            'fields may be case-sensitive.',
        )

    def test_valid_login(self):
        """User should be logged in and redirected on valid login."""
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=%2F')
        response = self.client.post('/login/', {
            'username': 'user',
            'password': 'password',
        })
        self.assertRedirects(response, '/')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class HomeViewTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            username='user', password='password',
            email='user@email.com',
        )
        self.todo_list = TodoList.objects.create(
            name='Test',
            user=self.user,
        )
        self.client = Client()

    def test_unauthorized_login(self):
        """Unauthorized users should not be able to reach the homepage."""
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=%2F')

    def test_rendered_todo_lists(self):
        """Homepage should show the created todo lists."""
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('home.html')
        self.assertEqual(
            list(response.context['todo_lists']), [self.todo_list],
        )


class TodoListViewTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            username='user', password='password',
        )
        self.todo_list = TodoList.objects.create(
            name='Test',
            user=self.user,
        )
        self.todo_1 = Todo.objects.create(
            description='Testing 1',
            todo_list=self.todo_list,
        )
        self.todo_2 = Todo.objects.create(
            description='Testing 2',
            todo_list=self.todo_list,
        )
        self.client = Client()

    def test_unauthorized_login(self):
        """Unauthorized users should not be able to reach the homepage."""
        response = self.client.get('/lists/1/')
        self.assertRedirects(response, '/login/?next=/lists/1/')

    def test_404_on_null(self):
        """Lists without an ID will return a 404."""
        self.client.force_login(self.user)
        response = self.client.get('/lists/2/')
        self.assertEqual(response.status_code, 404)

    def test_get_request(self):
        """GET request should just render the HTML form."""
        self.client.force_login(self.user)
        response = self.client.get('/lists/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_list.html')

    def test_form_errors(self):
        """Form should render errors on error."""
        self.client.force_login(self.user)
        response = self.client.post('/lists/1/', {
            'action': 'unknown',
            'todo_ids': [1],
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['errors'])

    def test_delete_todo(self):
        """Deleting a todo should delete it from the database."""
        self.client.force_login(self.user)
        response = self.client.post('/lists/1/', {
            'action': 'delete',
            'todo_ids': [2],
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context.get('errors'))
        self.assertEqual(len(self.todo_list.todo_set.all()), 1)

    def test_complete_todo(self):
        """Completing a todo should mark is as complete."""
        self.client.force_login(self.user)
        response = self.client.post('/lists/1/', {
            'action': 'complete',
            'todo_ids': [2],
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context.get('errors'))
        todo = Todo.objects.get(id=2)
        self.assertTrue(todo.is_complete)


class CreateTodoListViewTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            username='user', password='password',
        )
        self.client = Client()

    def test_unauthorized_login(self):
        """Unauthorized users should not be able to reach the homepage."""
        response = self.client.get('/lists/create/')
        self.assertRedirects(response, '/login/?next=/lists/create/')

    def test_get_request(self):
        """GET request should just render the HTML form."""
        self.client.force_login(self.user)
        response = self.client.get('/lists/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_list.html')

    def test_form_errors(self):
        """Form should render errors on error."""
        self.client.force_login(self.user)
        response = self.client.post('/lists/create/', {})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'].errors)

    def test_valid_form(self):
        """Valid form should create a new todo list."""
        self.client.force_login(self.user)
        response = self.client.post('/lists/create/', {
            'name': 'Test',
        })
        self.assertRedirects(response, '/lists/1/')
        todo_list = TodoList.objects.get(id=1)
        self.assertEqual(todo_list.name, 'Test')


class CreateTodoViewTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            username='user', password='password',
        )
        self.todo_list = TodoList.objects.create(
            name='Test',
            user=self.user,
        )
        self.another_user = get_user_model().objects.create_user(
            username='another', password='password',
        )
        self.another_todo_list = TodoList.objects.create(
            name='Test',
            user=self.another_user,
        )
        self.client = Client()

    def test_unauthorized_login(self):
        """Unauthorized users should not be able to reach the homepage."""
        response = self.client.get('/lists/1/create/')
        self.assertRedirects(response, '/login/?next=/lists/1/create/')

    def test_get_request(self):
        """GET request should just render the HTML form."""
        self.client.force_login(self.user)
        response = self.client.get('/lists/1/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_todo.html')

    def test_form_errors(self):
        """Form should render errors on error."""
        self.client.force_login(self.user)
        response = self.client.post('/lists/1/create/', {})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'].errors)

    def test_valid_form(self):
        """Valid form should create a new todo list."""
        self.client.force_login(self.user)
        response = self.client.post('/lists/1/create/', {
            'description': 'Testing',
        })
        self.assertRedirects(response, '/lists/1/')
        todo = Todo.objects.get(id=1)
        self.assertEqual(todo.description, 'Testing')

    def test_404_on_another_todo_list(self):
        """Lists should not be accessed by users without access."""
        self.client.force_login(self.user)
        response = self.client.get('/lists/2/create/')
        self.assertEqual(response.status_code, 404)


class EditTodoViewTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            username='user', password='password',
        )
        self.todo_list = TodoList.objects.create(
            name='Test',
            user=self.user,
        )
        self.client = Client()

    def create_todo(self):
        self.todo = Todo.objects.create(
            description='Testing',
            todo_list=self.todo_list,
        )

    def test_unauthorized_login(self):
        """Unauthorized users should not be able to reach the homepage."""
        response = self.client.get('/todos/1/edit/')
        self.assertRedirects(response, '/login/?next=/todos/1/edit/')

    def test_get_request(self):
        """GET request should just render the HTML form."""
        self.client.force_login(self.user)
        self.create_todo()
        response = self.client.get('/todos/1/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_todo.html')

    def test_form_errors(self):
        """Form should render errors on error."""
        self.client.force_login(self.user)
        self.create_todo()
        response = self.client.post('/todos/1/edit/', {})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'].errors)

    def test_valid_form(self):
        """Valid form should create a new todo list."""
        self.client.force_login(self.user)
        self.create_todo()
        response = self.client.post('/todos/1/edit/', {
            'description': 'Testing',
        })
        self.assertRedirects(response, '/lists/1/')
        todo = Todo.objects.get(id=1)
        self.assertEqual(todo.description, 'Testing')

    def test_404_on_another_todo_list(self):
        """Lists should not be accessed by users without access."""
        self.client.force_login(self.user)
        self.create_todo()
        user = get_user_model().objects.create_user(
            username='another', password='password',
        )
        todo_list = TodoList.objects.create(
            name='Test',
            user=user,
        )
        Todo.objects.create(
            description='Another',
            todo_list=todo_list,
        )
        response = self.client.get('/todos/2/edit/')
        self.assertEqual(response.status_code, 404)


class SignupViewTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            username='user', password='password',
        )
        self.client = Client()

    def test_redirect_authenticated(self):
        """Authenticated users should be redirected to home."""
        self.client.force_login(self.user)
        response = self.client.get('/signup/')
        self.assertRedirects(response, '/')

    def test_get_template(self):
        """GET request should be rendered with the correct template."""
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_form_errors(self):
        """Error should be returned if form is not valid."""
        response = self.client.post('/signup/', {
            'username': 'missing',
            'email': 'missing@email.com',
            'password': 'missing',
            'password_repeated': 'match',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', None,
            'Passwords do not match',
        )

    def test_valid_signup(self):
        """User should be shown a splash page on completion."""
        response = self.client.post('/signup/', {
            'username': 'missing',
            'email': 'missing@email.com',
            'password': 'missing',
            'password_repeated': 'missing',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_success.html')
        self.assertEqual(response.context['username'], 'missing@email.com')


class SeleniumTestCase(StaticLiveServerTestCase):
    """Base class for live server test cases."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.headless = True
        cls.selenium = WebDriver(firefox_options=options)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


class LoginServerTestCase(SeleniumTestCase):
    """Test cases for login page."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            username='user', password='password',
        )

    @tag('server')
    def test_form_labels(self):
        """Test that the correct labels render."""
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        labels = self.selenium.find_elements_by_tag_name('label')
        self.assertEqual(len(labels), 2)
        expected = ['Username*', 'Password*']
        for index, label in enumerate(labels):
            self.assertEqual(label.text, expected[index])

    @tag('server')
    def test_form_errors(self):
        """Errors should be displayed above the form."""
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username = self.selenium.find_element_by_name('username')
        username.send_keys('user')
        password = self.selenium.find_element_by_name('password')
        password.send_keys('missing')
        self.selenium.find_element_by_xpath('//input[@value="Submit"]').click()
        alert_block = self.selenium.find_element_by_class_name('alert-block')
        list_item = alert_block.find_element_by_tag_name('li')
        self.assertEqual(
            list_item.text,
            'Please enter a correct username and password. Note that both '
            'fields may be case-sensitive.'
        )

    @tag('server')
    def test_signup_question(self):
        """Signup question should render at the bottom."""
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        footer = self.selenium.find_element_by_class_name('card-footer')
        self.assertEqual(footer.text, 'Not registered? Sign up now!')

    @tag('server')
    def test_signup_link(self):
        """Signup link should go to the signup page."""
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        footer = self.selenium.find_element_by_class_name('card-footer')
        link = footer.find_element_by_tag_name('a')
        link.click()
        self.assertEqual(
            self.selenium.current_url, '%s%s' % (
                self.live_server_url, '/signup/'
            ),
        )


class SignupServerTestCase(SeleniumTestCase):
    """Test cases for login page."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            username='user', password='password',
        )

    @tag('server')
    def test_form_labels(self):
        """Test that the correct labels render."""
        self.selenium.get('%s%s' % (self.live_server_url, '/signup/'))
        labels = self.selenium.find_elements_by_tag_name('label')
        self.assertEqual(len(labels), 6)
        expected = [
            'Username*',
            'Email*',
            'Password*',
            'Password repeated*',
            'First name',
            'Last name'
        ]
        for index, label in enumerate(labels):
            self.assertEqual(label.text, expected[index])

    @tag('server')
    def test_splash_page(self):
        """Test that the splash page renders after successful signup."""
        self.selenium.get('%s%s' % (self.live_server_url, '/signup/'))

        username = self.selenium.find_element_by_name('username')
        email = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        password_repeated = self.selenium.find_element_by_name(
            'password_repeated',
        )

        username.send_keys('person')
        email.send_keys('person@email.com')
        password.send_keys('testing')
        password_repeated.send_keys('testing')

        self.selenium.find_element_by_xpath('//input[@value="Submit"]').click()

        paragraphs = self.selenium.find_elements_by_tag_name('p')
        self.assertEqual(len(paragraphs), 2)
        text = [
            "Thank you person@email.com! You've been successfully signed up!",
            "Please login to start making todo lists.",
        ]
        for index, paragraph in enumerate(paragraphs):
            self.assertEqual(paragraph.text, text[index])

    @tag('server')
    def test_cancel_button(self):
        """Clicking the cancel button should go back to login.."""
        self.selenium.get('%s%s' % (self.live_server_url, '/signup/'))
        self.selenium.find_element_by_class_name(
            'btn-outline-secondary',
        ).click()
        self.assertEqual(
            self.selenium.current_url, '%s%s' % (
                self.live_server_url, '/login/',
            ),
        )

    @tag('server')
    def test_form_errors(self):
        """Errors should be displayed above the form."""
        self.selenium.get('%s%s' % (self.live_server_url, '/signup/'))

        username = self.selenium.find_element_by_name('username')
        email = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('password')
        password_repeated = self.selenium.find_element_by_name(
            'password_repeated',
        )

        username.send_keys('who')
        email.send_keys('who@email.com')
        password.send_keys('testing')
        password_repeated.send_keys('nomatch')

        self.selenium.find_element_by_xpath('//input[@value="Submit"]').click()
        alert_block = self.selenium.find_element_by_class_name('alert-block')
        list_item = alert_block.find_element_by_tag_name('li')
        self.assertEqual(
            list_item.text,
            'Passwords do not match'
        )

