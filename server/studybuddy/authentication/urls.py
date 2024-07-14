from django.urls import path
from .views import SignupView, LoginView, ProfileView, AcceptFriendRequestView, DeclineFriendRequestView, LogoutView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('friend-request/<int:request_id>/accept/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friend-request/<int:request_id>/decline/', DeclineFriendRequestView.as_view(), name='decline-friend-request'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
