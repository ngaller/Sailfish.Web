'''
Created on Sep 6, 2009

@author: Nick
'''
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('auth.views',
    # Example:
    # (r'^sailfish/', include('sailfish.foo.urls')),
    url('^logout/$', 'logout', name='auth-logout'),
    url('^login/$', 'login', name='auth-login'),
)
