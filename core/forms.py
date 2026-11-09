from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from appraisal.models import FacultyProfile


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input-control',
            'placeholder': 'Username or Employee ID',
            'autofocus': True,
            'autocomplete': 'username',
            'id': 'id_username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input-control',
            'placeholder': 'Account Password',
            'autocomplete': 'current-password',
            'id': 'id_password',
        })
    )


class FacultyRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Rajesh'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sharma'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text="Login username (letters, numbers and @/./+/-/_ only)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. rsharma', 'autocomplete': 'username'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@university.edu', 'autocomplete': 'email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create strong password', 'id': 'id_reg_password', 'autocomplete': 'new-password'}),
        required=True,
        help_text="Minimum 8 characters with letters and numbers."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter password', 'id': 'id_reg_confirm_password', 'autocomplete': 'new-password'}),
        required=True
    )

    class Meta:
        model = FacultyProfile
        fields = [
            'employee_id',
            'department',
            'designation',
            'highest_qualification',
            'specialization',
            'date_of_joining',
            'experience_years',
            'contact_number',
        ]
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. FAC-CSE-005'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
            'highest_qualification': forms.Select(attrs={'class': 'form-select'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Artificial Intelligence, VLSI Design'}),
            'date_of_joining': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0', 'placeholder': '0.0'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 9876543210'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        reserved_usernames = {'admin', 'administrator', 'root', 'superuser', 'dean', 'hod', 'facultyos', 'system'}
        if username.lower() in reserved_usernames:
            raise forms.ValidationError("This username is reserved for system administration. Please choose a different username.")
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email

    def clean_employee_id(self):
        emp_id = self.cleaned_data.get('employee_id', '').strip().upper()
        if FacultyProfile.objects.filter(employee_id__iexact=emp_id).exists():
            raise forms.ValidationError("A faculty member with this Employee ID is already registered.")
        return emp_id

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match. Please re-enter identical passwords.")
            else:
                try:
                    temp_user = User(username=username or '', email=email or '')
                    validate_password(password, user=temp_user)
                except forms.ValidationError as error:
                    self.add_error('password', error)

        return cleaned_data
