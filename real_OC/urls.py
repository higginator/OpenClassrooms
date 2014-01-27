from django.conf.urls import patterns, include, url
from real_OC.views import home_page, get_data, about, buildings_list, contact
from real_OC.helpers import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'real_OC.views.home', name='home'),
    # url(r'^real_OC/', include('real_OC.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home_page),
    url(r'^about/$', about),
    url(r'^buildings/$', buildings_list),
    url(r'^contact/$', contact),
    #url(r'^get_data/$', determine_request),
)
