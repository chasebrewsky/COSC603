from django import forms
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from todo.models import TodoList, Todo


class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_repeated = forms.CharField(
        widget=forms.PasswordInput(),
    )
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password_repeated']:
            raise forms.ValidationError("Passwords do not match")

    def clean_username(self):
        user_model = get_user_model()
        username = self.cleaned_data['username']
        username_exists = user_model.objects.filter(username=username).exists()
        if username_exists:
            raise forms.ValidationError("User with username already exists")
        return username

    def clean_email(self):
        user_model = get_user_model()
        email = self.cleaned_data['email']
        email_exists = user_model.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError("User with email already exists")
        return email


class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['name']


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        exclude = ['todo_list', 'is_complete']


class TodoBulkEditForm(forms.Form):
    action = forms.ChoiceField(
        choices=(('complete', 'complete'), ('delete', 'delete')),
    )

    def __init__(self, queryset: QuerySet, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['todo_ids'] = forms.ModelMultipleChoiceField(queryset)

