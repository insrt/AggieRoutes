from django import forms

class LocationForm(forms.Form):
    origin = forms.CharField(label='origin', max_length=100)
    dest = forms.CharField(label='dest', max_length=100)