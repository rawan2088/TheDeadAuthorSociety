# authentication/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# to make the user still logged in after a password change  
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth import get_user_model

User = get_user_model()  # this is All.User, which has is_admin

# i put this in settings
# ADMIN_SECRET_CODE = "DEADAUTHOR2024"

from django.conf import settings

# the biggest change that happend to this file is that instead of falling back to the profile mode
# i made it fall back on the default one and then check if it is admin or normal user
def user_to_dict(user):
    """Reusable helper so every view returns the same shape."""
    return {
        'id':        user.id,
        'username':  user.username,
        'firstName': user.first_name,
        'lastName':  user.last_name,
        'email':     user.email,
        'role':      'admin' if user.is_admin else 'user',  # frontend still gets "role"
    }

@csrf_exempt
def signup_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data         = json.loads(request.body)
    first_name   = data.get('firstName', '').strip()
    last_name    = data.get('lastName', '').strip()
    username     = data.get('username', '').strip()
    password     = data.get('password', '')
    confirm_pass = data.get('confirmPassword', '')
    email        = data.get('email', '').strip()
    role         = data.get('role', 'user')
    admin_code   = data.get('adminCode', '')

    if password != confirm_pass:
        return JsonResponse({'error': 'Passwords do not match.'}, status=400)
    if len(password) < 6:
        return JsonResponse({'error': 'Password must be at least 6 characters.'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'That username is already taken.'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'That email is already registered.'}, status=400)
    if role == 'admin' and admin_code != settings.ADMIN_SECRET_CODE:
        return JsonResponse({'error': 'Invalid admin code.'}, status=403)

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user.is_admin = (role == 'admin')  # ← set is_admin directly on the user
    user.save()

    return JsonResponse({'message': 'Account created successfully!'}, status=201)


@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=401)

    data     = json.loads(request.body)
    username = data.get('username', '').strip()
    password = data.get('password', '')

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'Invalid username or password.'}, status=401)

    login(request, user)
    return JsonResponse({'message': 'Login successful', 'user': user_to_dict(user)})


@csrf_exempt
def logout_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})


def me_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not logged in'}, status=401)
    return JsonResponse(user_to_dict(request.user))


@csrf_exempt
def update_profile_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not logged in'}, status=401)
    if request.method != 'PUT':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)
    user = request.user

    # user.first_name = data.get('firstName', user.first_name)
    # user.last_name  = data.get('lastName',  user.last_name)
    user.username = data.get('username', user.username)
    user.email      = data.get('email',     user.email)

    new_password = data.get('newPassword', '')
    current_password = data.get('currentPassword', '')
    if new_password:
        if not user.check_password(current_password):
            return JsonResponse({'error': 'Current password is incorrect.'}, status=400)
        user.set_password(new_password)
        update_session_auth_hash(request, user) 

    user.save()
    return JsonResponse({'message': 'Profile updated', 'user': user_to_dict(user)})


