from django.urls import path
from chat import views
from chat.views import ChatListView, ChatDetailView, SendMessageView


urlpatterns = [
    path('',views.home_chat, name="home_chat"),
    path('chat/', ChatListView.as_view(), name='chat_list'),
    path('chat/<str:username>/', ChatDetailView.as_view(), name='chat_detail'),
    path('send_message/', SendMessageView.as_view(), name='send_message'),
]