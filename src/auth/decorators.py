"""
Decorators can be applied to a view to require that a user be logged in.
"""

from . import get_current_user, get_login_url
from django.http import HttpResponseRedirect

def login_required(view_func):
    def check_login(request, *args, **kwargs):
        user = get_current_user(request)
        if not user:
            return HttpResponseRedirect(get_login_url(request))
        return view_func(request, *args, **kwargs)
    return check_login
