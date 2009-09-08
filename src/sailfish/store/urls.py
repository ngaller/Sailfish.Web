from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('sailfish.store.views',
    # Example:
    # (r'^sailfish/', include('sailfish.foo.urls')),
    url('^$', 'index', name='store-index'),
    (r'^create/(?P<keyname>\w+)$', 'create'),
    (r'^details/$', 'details_search'),
    (r'^details/(?P<id>\w+)$', 'details'),
    (r'^purchase/$', 'purchase_search'),
    (r'^purchase/(?P<id>\w+)$', 'purchase'),
    (r'^activate/$', 'activate'),
    url(r'^thankyou/(?P<txid>\w+)$', 'thankyou', name="store-thankyou"),
    url(r'^paypal_ipn/$', 'paypal_ipn', name="store-paypal_ipn"),
    url(r'^edit/(?P<id>\w+)$', 'edit', name='store-edit'),
)
