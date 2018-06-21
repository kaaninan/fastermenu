from django import forms
from menu.models import *

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = (
            'name',
        )
