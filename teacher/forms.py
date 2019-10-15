from django import forms
from django.utils.translation import gettext as _

class SchoolSearchForm(forms.Form):
    name = forms.CharField(label=_('School name'), required=False)
    city = forms.CharField(label=_('City'), required=False)
    state = forms.CharField(label=_('State'), required=False, max_length=2)
    zip = forms.CharField(label=_('ZIP'), required=False, max_length = 5)