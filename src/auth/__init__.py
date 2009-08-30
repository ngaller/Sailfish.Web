"""
Simple authentication wrapper.

Configured using AUTHENTICATION_BACKENDS, a list of classes which must define 
the following methods:
 * get_current_user(request): retrieve the current user for the request
 * get_login_url(request): return a login url to which we can redirect the 
 client to log them in, if suitable for the request (return None if not
 applicable)
"""

from django.core.exceptions import ImproperlyConfigured
import models

def load_backend(path):
    """
    This loads the backends configured in the AUTHENTICATION_BACKENDS setting
    (same code and setting as for the Django backends)
    """
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = __import__(module, {}, {},  [attr])
    except ImportError, e:
        raise ImproperlyConfigured, 'Error importing authentication backend %s: %s"' % (module, e)
    except ValueError, e:
        raise ImproperlyConfigured, 'Error importing authentication backends.  Is AUTHENTICATION_BACKENDS a correctly defined list or tuple?'
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured, 'Module "%s" does not define a "%s" authentication backend' % (module, attr)
    return cls()

def get_backends():
    from django.conf import settings
    backends = []
    for backend_path in settings.AUTHENTICATION_BACKENDS:
        backends.append(load_backend(backend_path))
    if not backends:
        raise ImproperlyConfigured, "The AUTHENTICATION_BACKENDS setting must be defined."
    return backends

def get_current_user(request):
    """
    Return current user, or None if not currently logged in.
    """
    for backend in get_backends():
        val = backend.get_current_user(request)
        if val:
            return val
    return None

def get_login_url(request):
    """
    Form a login url for the request.
    """
    for backend in get_backends():
        val = backend.get_login_url(request)
        if val:
            return val
    return None

def context_processor(request):
    return {'user': get_current_user(request)}
