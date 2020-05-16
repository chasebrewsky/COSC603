from django.conf import settings
from django.shortcuts import redirect


def anonymous_required(func):
    def wrapped_view(request, *args, **kwargs):
        redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL)
        if request.user.is_authenticated:
            return redirect(redirect_to)
        return func(request, *args, **kwargs)
    return wrapped_view
