from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.db.transaction import commit

from django.contrib.auth.models import User


# I wrote this code

# Form to create a new user
class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Required. Enter your first name.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required. Enter your last name.")
    email = forms.EmailField(max_length=254, required=True, help_text="Required. Enter a valid email address.")
    profile_image = forms.ImageField(required=False, help_text="Optional. Upload a profile picture.")
    date_of_birth = forms.DateField(required=False, help_text="Optional. Enter your date of birth.",
                                    widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_image', 'date_of_birth']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Email is readonly and password is hidden
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['password'].widget = forms.HiddenInput()

    def clean_email(self):
        return self.initial['email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.profile_image = self.cleaned_data.get('profile_image')

        if commit:
            user.save()
        return user

# end of code I wrote
