from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm

from hashlib import sha1

class LoginForm(forms.Form):
    username = forms.CharField(label = _('Username'), widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    password = forms.CharField(label = _('Password'), widget = forms.PasswordInput)

class RegistrationForm(forms.Form):
    username = forms.CharField(label = _('Username'), widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    first_name = forms.CharField(label = _('First name'))
    age = forms.IntegerField(label = _('Age'), min_value=1, max_value=100)
    email = forms.EmailField(label = _('Email address'))
    user_type_choices = (('student',_('Student')),('teacher',_('Teacher')))
    user_type = forms.ChoiceField(label = _('I am a...'), choices = user_type_choices)
    password1 = forms.CharField(label = _('Password'), widget = forms.PasswordInput)
    password2 = forms.CharField(label = _('Confirm password'), help_text=_('Enter the same password as above, for verification.'), widget = forms.PasswordInput)
    terms = forms.BooleanField(label = _('I agree to the <a href="https://showcaseedu.com/terms">Terms of Service</a> and <a href="https://showcaseedu.com/privacy">Privacy Policy</a>. If I am under 13 years of age, I confirm that I have my parent or legal guardian\'s permission to use Showcase.'))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            get_user_model().objects.get(username = username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(_('This username is already in use, please try another.'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_hash = sha1(email.encode()).hexdigest()
        age = self.cleaned_data.get('age')
        try:
            get_user_model().objects.get(email = email)
            get_user_model().objects.get(email = email_hash)
        except get_user_model().DoesNotExist:
            if age >= 13:
                return email
            else:
                return email_hash
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

class PasswordResetFormCoppa(PasswordResetForm):
        def get_users(self, email):
            email_hash = sha1(email.encode()).hexdigest()
            adult_users = get_user_model()._default_manager.filter(**{
                '%s__iexact' % get_user_model().get_email_field_name(): email,
                'is_active': True,
            })
            child_users = get_user_model()._default_manager.filter(**{
                '%s__iexact' % get_user_model().get_email_field_name(): email_hash,
                'is_active': True,
            })
            active_users = adult_users | child_users
            return (u for u in active_users if u.has_usable_password())