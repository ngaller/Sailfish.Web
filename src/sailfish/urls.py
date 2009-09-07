from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^sailfish/', include('sailfish.foo.urls')),
    ('^$', direct_to_template, { 'template': 'home.html' }),
    ('^contact/$', 'sailfish.views.contact' ),
    ('^store/', include('sailfish.store.urls')),
    ('^auth/', include('auth.urls')),
    ('^(.*.html)$', direct_to_template),

    # Media (this is only used for dev since in production it will be 
    # aliased)
    ('^media/(.*)$', 'django.views.static.serve',
        { 'document_root': '/home/nico/django/sailfish/media' }),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
