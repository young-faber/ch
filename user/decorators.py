from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


from django.shortcuts import redirect, render

def verified_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_verified:
            return view_func(request, *args, **kwargs)
        return redirect("main:verification")
    return wrapper