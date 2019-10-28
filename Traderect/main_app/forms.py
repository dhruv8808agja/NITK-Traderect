from django import forms
from .models import *

class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photos
        fields = ['photoid', 'photofile','description','ownerid']
