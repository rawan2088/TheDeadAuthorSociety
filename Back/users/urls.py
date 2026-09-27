# accounts/urls.py
from django.urls import path
from . import views

# todo: reset password
urlpatterns = [
    path('auth/signup/',        views.UserCreateAPIView.as_view(),         name='signup'),
    # path('auth/login/',         views.login_view,           name='login'), # no longer useful
    # path('auth/logout/',        views.UserLogoutAPIView.as_view(),          name='logout'), # unnecessary
    
    # path('auth/refresh/',        views.logout_view,          name='logout'),
    
    # --- users urls ---
    path('users/me/',            views.UserProfileAPIView.as_view(),              name='me'),
    
    path('users/me/borrowed',            views.UserBorrowedListAPIView.as_view(),              name='me'),
    
    # for puplic users
    # path('users/<int:id>',            views.me_view,              name='me'),
    #// path('me/update/',     views.update_profile_view,  name='update_profile'),
]