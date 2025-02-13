from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, PasswordResetForm
from django.contrib import messages
from .models import User
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from myapp.utils import send_activation_email, send_reset_password_email
from django.contrib.auth.forms import SetPasswordForm



def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif request.user.is_staffmember:
            return redirect('staff_dashboard')
        return redirect('home')
    return render(request,'myapp/home.html')

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif request.user.is_staffmember:
            return redirect('staff_dashboard')
        return redirect('home')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            if request.user.is_superuser:
                return redirect('admin_dashboard')
            elif request.user.is_staffmember:
                print(request.user)
                return redirect('staff_dashboard')
    else:
        form = LoginForm()

    return render(request, 'myapp/login.html',{"form":form})


def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = reverse(
                    'password_reset_confirm',
                    kwargs={'uidb64': uidb64, 'token': token},
                )
                absolute_reset_url = f"{request.build_absolute_uri(reset_url)}"
                send_reset_password_email(user.email, absolute_reset_url)
            messages.success(
                request, (
                    "We have sent you a password reset link. Please check your email.")
            )
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'myapp/password_reset.html', {'form': form})

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            messages.error(request, ('This link has expired or is invalid.'))
            return redirect('password_reset')

        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, ('Your password has been successfully reset.')
                )
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
        else:
            form = SetPasswordForm(user)

        return render(
            request, 'myapp/password_reset_confirm.html', {
                'form': form, 'uidb64': uidb64, 'token': token}
        )

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, (
            'An error occurred. Please try again later.'))
        return redirect('password_reset')
