from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from authentication.forms import CustomUserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect


# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the newly registered user (optional).
            login(request, user)
            # Redirect to a success page or perform other actions upon successful registration.
            return redirect('/')
    else:
        form = CustomUserCreationForm()

    # If the form is invalid or it's a GET request (initial page load),
    # you can access form errors.
    errors = form.errors.values()
    registration_non_field_errors = form.non_field_errors()
    return render(request, 'auth/register.html',
                  {'form': form, 'errors': errors})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to a success page or do other actions upon successful login.
            return redirect('/')
    else:
        form = AuthenticationForm()

    # If the form is invalid or it's a GET request (initial page load),
    # you can access form.errors to get login errors.
    errors = form.errors.get('__all__')

    return render(request, 'auth/login.html',
                  {'form': form, 'errors': errors})


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('login')
