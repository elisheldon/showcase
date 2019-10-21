from django import forms
from django.utils.translation import gettext as _
from django.core.validators import URLValidator

from teacher.models import School

# https://stackoverflow.com/questions/49983328/cleanest-way-to-allow-empty-scheme-in-django-urlfield
class OptionalSchemeURLValidator(URLValidator):
    def __call__(self, value):
        if '://' not in value:
            value = 'http://' + value
        super(OptionalSchemeURLValidator, self).__call__(value)

class AddForm(forms.Form):
    sub_item_type_choices = (('link', _('Link')),('drive', _('Choose from Google Drive')),('onedrive', _('Choose from OneDrive')), ('gallery', _('Upload photos')),('document', _('Upload a document')))
    sub_item_type = forms.ChoiceField(label = _('Type'), choices = sub_item_type_choices)

    # link inputs
    url = forms.CharField(label = _('URL*'), required=False, validators=[OptionalSchemeURLValidator()], help_text=_('Files you choose will have a shareable link generated if necessary.'), widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    image = forms.CharField(widget = forms.HiddenInput(), required=False)

    # gallery inputs
    photos = forms.ImageField(label = _('Photos* (max size 5MB each)'), widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    #  file inputs
    file = forms.FileField(
        required=False,
        label = _('Document* (max size 2MB)'),
        widget=forms.FileInput(attrs={'accept':'.doc, .docx, .htm, .html, .odt, .pdf, .xls, .xlsx, .ods, .ppt, .pptx, .txt, .pages, .numbers, .key'})
    )

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

class SettingsForm(forms.Form):
    PF_PUBLIC_CHOICES = (
        (True, 'Public'),
        (False, 'Private')
    )
    pf_public = forms.ChoiceField(choices = PF_PUBLIC_CHOICES, label=_('Showcase visibility'), widget=forms.Select(), help_text=_('When your Showcase is public, it can be viewed by anyone who visits '), required=False)
    code = forms.CharField(label=_('School code'), required=False, max_length=6)
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            try:
                school = School.objects.get(student_code = code)
            except:
                raise forms.ValidationError(
                    _('That school code is not valid, please try another.'),
                )
        return code