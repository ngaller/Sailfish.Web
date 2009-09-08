from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('sailfish.contactloader.views',
    # Example:
    # (r'^sailfish/', include('sailfish.foo.urls')),
    url(r'^$', 'index'),
    url(r'^download/.*\.csv$', 'download'),
)
