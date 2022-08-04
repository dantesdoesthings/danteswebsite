from django.contrib.auth import models, password_validation
from django import forms
from django.contrib.auth import authenticate
from .models import User


class UserRegistrationForm(forms.ModelForm):
    name = forms.CharField(label='Display Name', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(
        label='Password',
        min_length=8,
        max_length=64,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        min_length=8,
        max_length=64,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text='Enter the same password as before, for verification.',
    )

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'password2')


class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Invalid credentials')


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'name', )

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email already in use')
