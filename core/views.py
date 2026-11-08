from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import LoginForm, FacultyRegistrationForm
from appraisal.models import FacultyProfile


def home_view(request):
    """
    Public landing page for the Faculty Self-Appraisal Portal.
    """
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    return render(request, 'core/home.html')


def login_view(request):
    """
    Unified login view for faculty and administration.
    """
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_emp_id = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']

            # Try authenticating by username first
            user = authenticate(request, username=username_or_emp_id, password=password)

            # If failed, check if the entered credential was an employee_id
            if user is None:
                try:
                    profile = FacultyProfile.objects.select_related('user').get(employee_id__iexact=username_or_emp_id)
                    user = authenticate(request, username=profile.user.username, password=password)
                except FacultyProfile.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                return redirect('dashboard_redirect')
            else:
                messages.error(request, "Invalid username/Employee ID or password. Please try again.")
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    """
    Safely logs out user and returns to login page.
    """
    logout(request)
    messages.info(request, "You have been securely logged out.")
    return redirect('login')


def register_faculty_view(request):
    """
    Registration page for new faculty members.
    """
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = FacultyRegistrationForm(request.POST)
        if form.is_valid():
            # Create the Django User
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create the FacultyProfile
            faculty_profile = form.save(commit=False)
            faculty_profile.user = user
            faculty_profile.save()

            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors in the registration form below.")
    else:
        form = FacultyRegistrationForm()

    return render(request, 'core/register.html', {'form': form})


@login_required
def dashboard_redirect_view(request):
    """
    Directs the user to their appropriate dashboard based on permissions and role.
    """
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')
    elif hasattr(request.user, 'faculty_profile'):
        return redirect('faculty_dashboard')
    else:
        # User without faculty profile and not admin - handle gracefully
        messages.warning(request, "Your account does not have an associated faculty profile. Please contact the administrator.")
        return redirect('login')


@login_required
def change_password_view(request):
    """
    Secure password change view requiring current password verification.
    Safely preserves active session authentication.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been changed successfully!")
            return redirect('dashboard_redirect')
        else:
            messages.error(request, "Please correct the password errors below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'core/change_password.html', {'form': form})

