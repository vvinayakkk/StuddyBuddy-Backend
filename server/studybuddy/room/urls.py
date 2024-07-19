# room/urls.py

from django.urls import path
from .views import room_list, room_messages, create_room, send_message

urlpatterns = [
    path('rooms/', room_list, name='room_list'),
    path('rooms/<int:room_id>/messages/', room_messages, name='room_messages'),
    path('rooms/create/', create_room, name='create_room'),
    path('messages/send/', send_message, name='send_message'),
]
