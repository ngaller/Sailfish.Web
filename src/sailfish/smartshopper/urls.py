'''
Created on Oct 22, 2009

@author: Nick
'''
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('sailfish.smartshopper.views',
    # Example:
    # (r'^sailfish/', include('sailfish.foo.urls')),
    url('^$', 'index', name='smartshopper-index'),
    url('^create/$', 'create'),
    url('^details/(?<list_id>.*)/$', 'details', name='smartshopper-details'),
    url('^add_item/(?<list_id>.*)/$', 'add_item'),
)