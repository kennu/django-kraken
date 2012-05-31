from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from users.forms import EmailUserCreationForm

# Enable the admin:
from django.contrib import admin
admin.autodiscover()

# Home views
urlpatterns = patterns('home.views',
    url(r'^$', 'home', name='home'),
)

# User views
urlpatterns += patterns('users.views',
    url(r'^users/(?P<id>[^/]+)$', 'profile', name='user_profile'),
    url(r'^me$', 'profile_me', name='user_profile_me'),
)

# Registration views
urlpatterns += patterns('registration.views',
    url(r'^accounts/register$', 'register', {'backend': 'registration.backends.default.DefaultBackend', 'form_class':EmailUserCreationForm}, name='registration_register'),
    url(r'^accounts/register/complete$', direct_to_template, {'template': 'registration/registration_complete.html'}, name='registration_complete'),
    url(r'^accounts/register/closed$', direct_to_template, {'template': 'registration/registration_closed.html'}, name='registration_disallowed'),
    url(r'^accounts/activate/complete$', direct_to_template, {'template': 'registration/activation_complete.html'}, name='registration_activation_complete'),
    url(r'^accounts/activate/(?P<activation_key>\w+)$', 'activate', {'backend': 'registration.backends.default.DefaultBackend'}, name='registration_activate'),
)

# Authentication views
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^accounts/login$', 'login', {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^accounts/logout$', 'logout', {'template_name': 'registration/logout.html'}, name='auth_logout'),
    url(r'^accounts/password/change$', 'password_change', name='auth_password_change'),
    url(r'^accounts/password/change/done$', 'password_change_done', name='auth_password_change_done'),
    url(r'^accounts/password/reset$', 'password_reset', name='auth_password_reset'),
    url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$', 'password_reset_confirm', name='auth_password_reset_confirm'),
    url(r'^accounts/password/reset/complete$', 'password_reset_complete', name='auth_password_reset_complete'),
    url(r'^accounts/password/reset/done$', 'password_reset_done', name='auth_password_reset_done'),
)

# Django system views
urlpatterns += patterns('',
    # Enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
