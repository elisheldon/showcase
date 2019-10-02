from django import forms
from django.utils.translation import gettext as _
from django.core.validators import URLValidator

# https://stackoverflow.com/questions/49983328/cleanest-way-to-allow-empty-scheme-in-django-urlfield
class OptionalSchemeURLValidator(URLValidator):
    def __call__(self, value):
        if '://' not in value:
            value = 'http://' + value
        super(OptionalSchemeURLValidator, self).__call__(value)

class AddForm(forms.Form):
    sub_item_type_choices = (('link', _('Link')),('gallery', _('Photos')))
    sub_item_type = forms.ChoiceField(label = _('Type'), choices = sub_item_type_choices)

    # link inputs
    url = forms.CharField(label = _('URL*'), required=False, validators=[OptionalSchemeURLValidator()], widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    image = forms.CharField(widget = forms.HiddenInput(), required=False)

    # gallery inputs
    photos = forms.ImageField(label = _('Photos*'), widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    title = forms.CharField(label = _('Title'), max_length=128)
    description = forms.CharField(label = _('Description'), widget=forms.Textarea(attrs={'rows':3}), required=False, max_length=256)

    def clean_url(self):
        url = self.cleaned_data.get('url')
        sub_item_type = self.cleaned_data.get('sub_item_type')
        if url == '' and sub_item_type == 'link':
            raise forms.ValidationError(
                _('Make sure to include the URL you want to add.'),
            )
        if url[0:4] != 'http':
            url = 'http://' + url
        return url