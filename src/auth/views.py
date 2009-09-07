'''
Created on Sep 6, 2009

@author: Nick
'''

from django.http import HttpResponseRedirect
from auth import get_current_user, get_logout_url
from auth.decorators import login_required

@login_required
def login(request):
    return HttpResponseRedirect(request.build_absolute_uri("/"))

def logout(request):
    if get_current_user(request):
        return HttpResponseRedirect(get_logout_url(request))
    return HttpResponseRedirect(request.build_absolute_uri("/"))