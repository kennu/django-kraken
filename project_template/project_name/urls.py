from django.conf.urls.defaults import patterns, include, url

# Enable the admin:
from django.contrib import admin
admin.autodiscover()

# Home views
urlpatterns = patterns('home.views',
    url(r'^$', 'home', name='home'),
)

# Django system views
urlpatterns += patterns('',
    # Enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
