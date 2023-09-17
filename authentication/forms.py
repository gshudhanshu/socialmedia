from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.transaction import commit
from django.contrib.auth.models import User


# I wrote this code
class CustomUserCreationForm(UserCreationForm):
    # Additional fields for the User model
    first_name = forms.CharField(max_length=30, required=True, help_text="Required. Enter your first name.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required. Enter your last name.")
    email = forms.EmailField(max_length=254, required=True, help_text="Required. Enter a valid email address.")
    profile_image = forms.ImageField(required=False, help_text="Optional. Upload a profile picture.")
    date_of_birth = forms.DateField(required=False, help_text="Optional. Enter your date of birth.",
                                    widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'profile_image', 'email', 'password1',
                  'password2']

    def clean_username(self):
        # Check if the username is already in use
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already in use. Please choose a different one.")
        return username

    def clean_email(self):
        # Check if the email address is already in use
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use. Please use a different one.")
        return email

    def save(self, commit=True):
        # Create a new user
        user = super().save(commit=False)
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.profile_image = self.files.get('profile_image')
        if commit:
            user.save()
        return user
# end of code I wrote
