from django import forms
from .models import Data

class Newdata_form(forms.ModelForm):
    class Meta:
        model = Data
        exclude = ['user','final_outcome']
        
class Massdata_form(forms.Form):
    n = forms.IntegerField(min_value=1, max_value=500, label="Number of entries to generate")
    