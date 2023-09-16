from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from authentication.forms import CustomUserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect


# I wrote this code
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Auto Log the user in
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()

    # If the form is invalid, render the page with the form and errors
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
            # Redirect to a success page.
            return redirect('/')
    else:
        form = AuthenticationForm()

    # If the form is invalid, render the page with the form and errors
    errors = form.errors.get('__all__')
    return render(request, 'auth/login.html',
                  {'form': form, 'errors': errors})


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('login')
# end of code I wrote
