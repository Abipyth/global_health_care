from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def group_required(group_name):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            return redirect('login')  # Redirect unauthorized users
        return _wrapped_view
    return decorator
