from django import forms
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.contrib.auth.forms import UserCreationForm

from .models import Account

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=30, help_text = 'Required. Add a valid email address')
    class Meta:
        model = Account
        fields = ('email', 'password1', 'password2')

    def clean_password2(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            information = "The Passwords didn't Match!. Try Again."
            raise forms.ValidationError(information)
        return password2

class SignInForm(forms.Form):
    email = forms.EmailField(max_length=30, help_text = 'Required. Add a valid email address')
    password  = forms.CharField(label= 'Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        for field in (self.fields['email'],self.fields['password']):
            field.widget.attrs.update({'class': 'form-control '})

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not authenticate(email=email, password=password):
            information = 'The Username or Password is Incorrect!'
            raise forms.ValidationError(information)
        return password