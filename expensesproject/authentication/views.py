from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
import json

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.urls import reverse

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import AppTokenGenerator


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username is already in use, choose another one'}, status=409)

        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'email_error': 'Invalid email format'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email is already in use, choose another one'}, status=409)

        return JsonResponse({'email_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        context = {'fieldValues': request.POST}

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
            return render(request, 'authentication/register.html', context)

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use")
            return render(request, 'authentication/register.html', context)

        if len(password) < 6:
            messages.error(request, "Password is too short")
            return render(request, 'authentication/register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        token_generator = AppTokenGenerator()
        link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

        activate_url = f'https://{domain}{link}'

        email_subject = 'Activate your account'
        email_body = f'Hi {user.username},\n\nPlease use this link to verify your account:\n{activate_url}'
        
        email_message = EmailMessage(
            email_subject,
            email_body,
            'noreply@gmail.com',
            [email],
        )
        email_message.send(fail_silently=False)
        messages.success(request, "Account created successfully. Please check your email.")

        return redirect('register')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            token_generator = AppTokenGenerator()
            if not token_generator.check_token(user, token):
                messages.error(request, "Account activation link is invalid or expired.")
                return redirect('login')

            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as e:
            print(f"Error in VerificationView: {e}")
            messages.error(request, "Invalid activation link.")

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Please fill in all fields')
            return render(request, 'authentication/login.html')

        user = auth.authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, f'Welcome, {user.username}! You are now logged in.')
                return redirect('http://127.0.0.1:8000/')  
            else:
                messages.error(request, 'Account is not active, Please check your email')
                return render(request, 'authentication/login.html')

        messages.error(request, 'Invalid credentials, try again')
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request,'You have been logged out')
        return redirect('login')