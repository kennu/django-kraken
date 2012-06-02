from emailusernames.forms import EmailUserCreationForm as OriginalEmailUserCreationForm, EmailAuthenticationForm as OriginalEmailAuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django import forms

# Override to be compatible with django-registration and to set autofocus.
class EmailUserCreationForm(OriginalEmailUserCreationForm):
    email = forms.EmailField(label=_("Email"), max_length=75, widget=forms.TextInput(attrs={'class':'autofocus'}))
    def clean(self):
        cleaned_data = super(EmailUserCreationForm, self).clean()
        if cleaned_data.has_key('email'):
            cleaned_data['username'] = cleaned_data['email']
        return cleaned_data

# Override to fix order of email and password fields and to set autofocus.
class EmailAuthenticationForm(OriginalEmailAuthenticationForm):
    email = forms.EmailField(label=_("Email"), max_length=75, widget=forms.TextInput(attrs={'class':'autofocus'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['email', 'password']
