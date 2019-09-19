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
    title = forms.CharField(label = _('Title'))
    description = forms.CharField(widget=forms.Textarea, required=False)
    itemTypeChoices = (('link', _('Link')),('gallery', _('Photos')))
    itemType = forms.ChoiceField(label = _('Type'), choices = itemTypeChoices)

    # link inputs
    url = forms.CharField(label = _('URL'), required=False, validators=[OptionalSchemeURLValidator()])

    # gallery inputs
    tempLocation = forms.CharField(required=False)

    def clean_url(self):
        url = self.cleaned_data.get('url')
        itemType = self.cleaned_data.get('itemType')
        if url == '' and itemType == 'link':
            raise forms.ValidationError(
                _('Make sure to include the URL you want to add.'),
            )
        if url[0:3] != 'http':
            url = 'http://' + url
        return url

    def clean_tempLocation(self):
        tempLocation = self.cleaned_data.get('tempLocation')
        itemType = self.cleaned_data.get('itemType')
        if tempLocation == '' and itemType == 'gallery':
            raise forms.ValidationError(
                _('Make sure to include the tempLocation you want to add.'),
            )
        return tempLocation