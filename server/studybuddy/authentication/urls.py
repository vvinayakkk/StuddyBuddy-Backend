from django.urls import path
from .views import SignupView, LoginView, LogoutView, PasswordResetView, EmailVerificationView
from . import views

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('email-verify/', EmailVerificationView.as_view(), name='email_verify'),
    path('profile/', views.profile_view_get, name='profile_get'),
    path('profile/update/', views.profile_view_put, name='profile_put'),
    path('profile/image/', views.profile_image_update_view, name='profile_image_update'),
    path('profile/image2/', views.profile_view_get2, name='profile_view_get2'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request_view, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>/', views.decline_friend_request_view, name='decline_friend_request'),
]
