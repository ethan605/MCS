from django.conf.urls.defaults import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns("",
    # Examples:
    # url(r"^$", "MCS.views.home", name="home"),
    # url(r"^MCS/", include("MCS.foo.urls")),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r"^admin/doc/", include("django.contrib.admindocs.urls")),

    # Uncomment the next line to enable the admin:
    # url(r"^admin/", include(admin.site.urls)),

    url(r"^$", "system.views.index"),
    url(r"^signin/$","system.views.sign_in"),
    url(r"^signup/$", "system.views.signup"),
    url(r"^signup/success/$","system.views.success"),
    url(r"^admin/$","system.views.admin"),
    url(r"^usercp/$", "system.views.usercp"),
    url(r"^usercp/changepass/$", "system.views.changepass"),
    url(r"^signout/$", "system.views.sign_out"),
    url(r"^ajax/$", "system.views.ajax")
)
