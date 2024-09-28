from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from ELib.forms import SignupForm
from django.contrib.auth.views import LogoutView

def signupView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Automatically log in the user
            messages.success(request, 'Account created successfully!')
            return redirect('library')  # Redirect to the home page or another page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def logoutView(request):
    if request.method == 'POST':
        # If user confirms logout, call the built-in LogoutView
        return LogoutView.as_view()(request)
    
    # If not POST, just render the confirmation page
    return render(request, 'logout.html')