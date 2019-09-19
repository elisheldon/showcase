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
    title = forms.CharField(label = _('Title'), widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False)
    item_type_choices = (('link', _('Link')),('gallery', _('Photos')))
    item_type = forms.ChoiceField(label = _('Type'), choices = item_type_choices)

    # link inputs
    url = forms.CharField(label = _('URL*'), required=False, validators=[OptionalSchemeURLValidator()])

    # gallery inputs
    temp_location = forms.CharField(required=False)

    def clean_url(self):
        url = self.cleaned_data.get('url')
        item_type = self.cleaned_data.get('item_type')
        if url == '' and item_type == 'link':
            raise forms.ValidationError(
                _('Make sure to include the URL you want to add.'),
            )
        if url[0:3] != 'http':
            url = 'http://' + url
        return url

    def clean_tempLocation(self):
        temp_location = self.cleaned_data.get('temp_location')
        item_type = self.cleaned_data.get('item_type')
        if temp_location == '' and item_type == 'gallery':
            raise forms.ValidationError(
                _('Make sure to include the temp_location you want to add.'),
            )
        return temp_location