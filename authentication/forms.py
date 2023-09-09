from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Required. Enter your first name.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required. Enter your last name.")
    email = forms.EmailField(max_length=254, required=True, help_text="Required. Enter a valid email address.")
    image = forms.ImageField(required=False, help_text="Optional. Upload a profile picture.")
    date_of_birth = forms.DateField(required=False, help_text="Optional. Enter your date of birth.",
                                    widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'image', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already in use. Please choose a different one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use. Please use a different one.")
        return email
