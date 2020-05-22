from django.contrib.auth import get_user_model, login as _login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404

from todo.decorators import anonymous_required
from todo.forms import SignupForm, TodoListForm, TodoForm, TodoBulkEditForm
from todo.models import TodoList, Todo


@anonymous_required
def login(request: HttpRequest):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if not form.is_valid():
            return render(request, 'login.html', {'form': form})
        _login(request, form.get_user())
        return redirect('/')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@anonymous_required
def signup(request: HttpRequest):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if not form.is_valid():
            return render(request, 'signup.html', {'form': form})
        user_model = get_user_model()
        user = user_model.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
        )
        return render(request, 'signup_success.html', {
            'username': user.get_full_name() or user.email,
        })
    form = SignupForm()
    return render(request, 'signup.html', {'form': form})


@login_required()
def home(request: HttpRequest):
    return render(request, 'home.html', {
        'todo_lists': TodoList.objects.filter(user=request.user).all()
    })


@login_required()
def view_list(request: HttpRequest, list_id: int = 0):
    todo_list = get_object_or_404(TodoList, pk=list_id)
    todos = todo_list.todo_set.filter(is_complete=False)
    completed_todos = todo_list.todo_set.filter(is_complete=True)
    context = {
        'todo_lists': TodoList.objects.filter(user=request.user).all(),
        'todo_list': todo_list,
        'todos': todos,
        'completed_todos': completed_todos,
    }
    if request.method == 'POST':
        form = TodoBulkEditForm(todos, request.POST)
        if not form.is_valid():
            context['errors'] = form.errors
            return render(request, 'view_list.html', context)
        if form.cleaned_data['action'] == 'delete':
            for todo in form.cleaned_data['todo_ids']:
                todo.delete()
        if form.cleaned_data['action'] == 'complete':
            for todo in form.cleaned_data['todo_ids']:
                todo.is_complete = True
                todo.save()
        return render(request, 'view_list.html', context)
    return render(request, 'view_list.html', context)


@login_required()
def create_list(request: HttpRequest):
    context = {
        'todo_lists': TodoList.objects.filter(user=request.user).all()
    }
    if request.method == 'POST':
        form = TodoListForm(request.POST)
        if not form.is_valid():
            context['form'] = form
            return render(request, 'create_list.html', context)
        todo_list = form.save(commit=False)
        todo_list.user = request.user
        todo_list.save()
        return redirect('view_list', todo_list.id)
    form = TodoListForm()
    context['form'] = form
    return render(request, 'create_list.html', context)


@login_required()
def create_todo(request: HttpRequest, list_id: int = 0):
    context = {
        'todo_lists': TodoList.objects.filter(user=request.user).all()
    }
    todo_list = get_object_or_404(TodoList, pk=list_id)
    if todo_list.user != request.user:
        raise Http404
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if not form.is_valid():
            context['form'] = form
            return render(request, 'create_todo.html', context)
        todo = form.save(commit=False)
        todo.todo_list = todo_list
        todo.save()
        return redirect('view_list', todo_list.id)
    form = TodoForm()
    context['form'] = form
    return render(request, 'create_todo.html', context)


@login_required()
def edit_todo(request: HttpRequest, todo_id: int = 0):
    context = {
        'todo_lists': TodoList.objects.filter(user=request.user).all()
    }
    todo = get_object_or_404(Todo, pk=todo_id)
    if todo.todo_list.user != request.user:
        raise Http404
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if not form.is_valid():
            context['form'] = form
            return render(request, 'edit_todo.html', context)
        todo = form.save()
        return redirect('view_list', todo.todo_list.id)
    form = TodoForm(instance=todo)
    context['form'] = form
    return render(request, 'edit_todo.html', context)

