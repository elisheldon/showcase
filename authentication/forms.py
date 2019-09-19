from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    username = forms.CharField(label = _('Username'), widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    password = forms.CharField(label = _('Password'), widget = forms.PasswordInput)

class RegistrationForm(forms.Form):
    username = forms.CharField(label = _('Username'), widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    first_name = forms.CharField(label = _('First name'))
    last_name = forms.CharField(label = _('Last name'))
    email = forms.EmailField(label = _('Email address'))
    user_type_choices = (('student',_('Student')),('teacher',_('Teacher')))
    user_type = forms.ChoiceField(label = _('I am a...'), choices = user_type_choices)
    password1 = forms.CharField(label = _('Password'), widget = forms.PasswordInput)
    password2 = forms.CharField(label = _('Confirm password'), help_text=_('Enter the same password as above, for verification.'), widget = forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            get_user_model().objects.get(username = username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(_('This username is already in use, please try another.'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            get_user_model().objects.get(email = email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(_('This email address is already associated with an account.'))

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError(
                _('Passwords do not match.'),
            )
        return password2