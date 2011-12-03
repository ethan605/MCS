from django.conf.urls.defaults import patterns, include, url
from MCS import system

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MCS.views.home', name='home'),
    # url(r'^MCS/', include('MCS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'system.views.home'),
    url(r'^signin/$','system.views.sign_in'),
    url(r'^shop/signup/$','system.views.shop_signup'),
    url(r'^admin/$','system.views.admin'),
    url(r'^success/$','system.views.success'),
)
