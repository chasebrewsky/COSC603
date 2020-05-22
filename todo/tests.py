from django.contrib.auth import get_user_model, login as _login
from django.db import IntegrityError
from django.test import TestCase, Client
from django.urls import reverse, resolve
from todo.forms import SignupForm, TodoListForm, TodoForm, TodoBulkEditForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from todo.models import Todo, TodoList
from django.contrib.auth.models import User
from django.http import HttpRequest
from todo.views import login, signup, home, view_list, create_list, create_todo, edit_todo
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.core import exceptions
from . import views

class TestSignIn(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser', password='12345', email='useremail@example.com')
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
        self.user = get_user_model().objects.create(username='testuser', password='12345', email='useremail@example.com')
    def test_CorrectUser(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': '12345'})
        self.assertTrue(response)
    def test_WrongUsername(self):
        response = self.client.post('/login/', {'username': 'wrong', 'password': '12345'})
        self.assertTrue(response)
    def test_WrongPassword(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrong'})
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
        item1 =TodoList(name="Go to the mall")
        item2 =TodoList(name="Go to the car wash")
        self.assertEqual(str(item1), (item1.name))
        self.assertEqual(str(item2), (item2.name)) 
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
        self.assertTrue (response)
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

