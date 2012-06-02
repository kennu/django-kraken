"""
Override the add- and change-form in the admin, to hide the username.
This is copied from django-email-as-username, but the permissions,
groups and password sections are removed to make it work with MongoDB.
"""
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from emailusernames.forms import EmailUserCreationForm, EmailUserChangeForm
from django.utils.translation import ugettext_lazy as _


class EmailUserAdmin(UserAdmin):
    add_form = EmailUserCreationForm
    form = EmailUserChangeForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    ordering = ('email',)


admin.site.unregister(User)
admin.site.register(User, EmailUserAdmin)


def __email_unicode__(self):
    return self.email

