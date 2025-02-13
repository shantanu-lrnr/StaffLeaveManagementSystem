from django import forms
from .models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100,required=True)
    password = forms.CharField(max_length=100,required=True)

    def clean(self):
        clean_data = super().clean()
        email = clean_data.get("email")
        password = clean_data.get("password")
        if email and password:
            user = authenticate(email=email,password=password)
            if not user:
                raise forms.ValidationError("Please enter the correct email and password.Note that both fields may be case-sensitive.")
            clean_data['user'] = user
        return clean_data


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if a user with this email exists
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                ('No account is associated with this email address.')
            )
        return email