from django import forms

class AddVideoForm(forms.Form):
    title = forms.CharField(max_length=225, required=True)
    url = forms.URLField(required=True)

