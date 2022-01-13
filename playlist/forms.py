from django import forms

class PlayListCreateForm(forms.Form):
    title = forms.CharField(max_length=225)