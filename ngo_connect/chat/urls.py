from django.urls import path
from chat import views
from chat.views import SendMessageView, ChatView, ChatWithUserView

urlpatterns = [
    path('',views.home_chat, name="home_chat"),
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('<str:username>/', ChatWithUserView.as_view(), name='chat_with'),
]