from emailusernames.forms import EmailUserCreationForm as OriginalEmailUserCreationForm

class EmailUserCreationForm(OriginalEmailUserCreationForm):
    def clean(self):
        cleaned_data = super(EmailUserCreationForm, self).clean()
        if cleaned_data.has_key('email'):
            cleaned_data['username'] = cleaned_data['email']
        return cleaned_data

