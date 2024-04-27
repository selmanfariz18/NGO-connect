from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from base.models import ngousers, Notifications
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from chat.models import Message
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.db.models import Q

# Create your views here.


def home_chat(request):
    return render(request, 'chat.html')

class SendMessageView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        receiver_username = request.POST.get('receiver')
        message_text = request.POST.get('message')
        receiver = User.objects.get(username=receiver_username)
        Message.objects.create(sender=request.user, receiver=receiver, message=message_text)
        return redirect('chat')

class ChatView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # Fetch messages where the user is either the sender or the receiver
        messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-timestamp')
        
        # Get distinct users involved in the messages
        users_messaged = User.objects.filter(
            Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
        ).distinct()

        return render(request, 'chat.html', {'messages': messages, 'users': users_messaged})
    
class ChatWithUserView(View):
    @method_decorator(login_required)
    def get(self, request, username, *args, **kwargs):
        other_user = User.objects.get(username=username)
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=other_user)) | 
            (Q(sender=other_user) & Q(receiver=request.user))
        ).order_by('timestamp')
        return render(request, 'chat_with_user.html', {'messages': messages, 'other_user': other_user})