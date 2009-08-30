from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('sailfish.store.views',
    # Example:
    # (r'^sailfish/', include('sailfish.foo.urls')),
    url('^$', 'index', name='store-index'),
    ('^create/$', 'create'),
    url('^edit/(?P<id>\w+)/$', 'edit', name='store-edit'),
)
