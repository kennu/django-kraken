from emailusernames.forms import EmailUserCreationForm as OriginalEmailUserCreationForm, EmailAuthenticationForm as OriginalEmailAuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django import forms

# Override to be compatible with django-registartion
class EmailUserCreationForm(OriginalEmailUserCreationForm):
    def clean(self):
        cleaned_data = super(EmailUserCreationForm, self).clean()
        if cleaned_data.has_key('email'):
            cleaned_data['username'] = cleaned_data['email']
        return cleaned_data

# Override to fix order of email and password fields.
class EmailAuthenticationForm(OriginalEmailAuthenticationForm):
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
