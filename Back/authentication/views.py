# accounts/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

ADMIN_SECRET_CODE = "DEADAUTHOR2024"  # secret code for admin signup

@csrf_exempt
def signup_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)

    first_name   = data.get('firstName', '').strip()
    last_name    = data.get('lastName', '').strip()
    username     = data.get('username', '').strip()
    password     = data.get('password', '')
    confirm_pass = data.get('confirmPassword', '')
    email        = data.get('email', '').strip()
    role         = data.get('role', 'user')
    admin_code   = data.get('adminCode', '')

    # --- Validations ---
    if password != confirm_pass:
        return JsonResponse({'error': 'Passwords do not match.'}, status=400)

    if len(password) < 6:
        return JsonResponse({'error': 'Password must be at least 6 characters.'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'That username is already taken.'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'That email is already registered.'}, status=400)

    # Only allow admin role if correct secret code is given
    if role == 'admin' and admin_code != ADMIN_SECRET_CODE:
        return JsonResponse({'error': 'Invalid admin code.'}, status=403)

    # --- Create user (Django hashes the password automatically) ---
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    Profile.objects.create(user=user, role=role)

    return JsonResponse({'message': 'Account created successfully!'}, status=201)


@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)
    username = data.get('username', '').strip()
    password = data.get('password', '')

    # authenticate() checks username + hashed password
    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({'error': 'Invalid username or password.'}, status=401)

    login(request, user)  # creates a session cookie

    profile = Profile.objects.get(user=user)
    return JsonResponse({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email,
            'role': profile.role,
        }
    })


@csrf_exempt
def logout_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    logout(request)  # destroys the session
    return JsonResponse({'message': 'Logged out successfully'})


def me_view(request):
    """Return the currently logged-in user's data."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not logged in'}, status=401)

    profile = Profile.objects.get(user=request.user)
    return JsonResponse({
        'id': request.user.id,
        'username': request.user.username,
        'firstName': request.user.first_name,
        'lastName': request.user.last_name,
        'email': request.user.email,
        'role': profile.role,
    })


@csrf_exempt
def update_profile_view(request):
    """Update the currently logged-in user's profile."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not logged in'}, status=401)

    if request.method != 'PUT':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)

    user = request.user
    user.first_name = data.get('firstName', user.first_name)
    user.last_name  = data.get('lastName', user.last_name)
    user.email      = data.get('email', user.email)

    # If they want to change password
    new_password = data.get('newPassword', '')
    if new_password:
        if len(new_password) < 6:
            return JsonResponse({'error': 'New password must be at least 6 characters.'}, status=400)
        user.set_password(new_password)

    user.save()

    profile = Profile.objects.get(user=user)
    return JsonResponse({
        'message': 'Profile updated',
        'user': {
            'id': user.id,
            'username': user.username,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email,
            'role': profile.role,
        }
    })