from django import forms

class LocationForm(forms.Form):
    origin = forms.CharField(label='Start Point', max_length=200)
    dest = forms.CharField(label='End Point', max_length=200)