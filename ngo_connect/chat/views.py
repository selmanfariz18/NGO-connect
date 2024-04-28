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
from django.db.models import OuterRef, Subquery, Max, Q, DateTimeField

# Create your views here.


def home_chat(request):
    return render(request, 'chat.html')

class ChatListView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # Get the latest timestamp for sent and received messages for each user
        last_sent = Message.objects.filter(
            sender=request.user,
            receiver=OuterRef('pk')
        ).order_by().values('receiver').annotate(
            latest=Max('timestamp')
        ).values('latest')

        last_received = Message.objects.filter(
            receiver=request.user,
            sender=OuterRef('pk')
        ).order_by().values('sender').annotate(
            latest=Max('timestamp')
        ).values('latest')

        # Annotate users with the latest interaction date using Subquery
        users = User.objects.annotate(
            last_interaction=Max(
                Subquery(last_sent, output_field=DateTimeField()),
                Subquery(last_received, output_field=DateTimeField())
            )
        ).filter(
            Q(sent_messages__receiver=request.user) |
            Q(received_messages__sender=request.user)
        ).exclude(username=request.user.username).order_by('-last_interaction')

        try:
            ngo_user = ngousers.objects.get(user=request.user)
        except ngousers.DoesNotExist:
            ngo_user = ngousers(user=request.user)
        users_list = User.objects.exclude(username=request.user.username).exclude(is_superuser=True)

        context = {
            'user_type' : ngo_user.user_type,
            'users': users,
            'all_users': users_list
        }

        return render(request, 'chat_list.html', context)

class ChatDetailView(View):
    @method_decorator(login_required)
    def get(self, request, username, *args, **kwargs):
        other_user = User.objects.get(username=username)
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=other_user)) | 
            (Q(sender=other_user) & Q(receiver=request.user))
        ).order_by('timestamp')
        return render(request, 'chat_detail.html', {'messages': messages, 'other_user': other_user})

class SendMessageView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        receiver_username = request.POST.get('receiver')
        message_text = request.POST.get('message')
        receiver = User.objects.get(username=receiver_username)
        Message.objects.create(sender=request.user, receiver=receiver, message=message_text)
        Notifications.objects.create(
            user=receiver,
            name="Message received",
            desc=f"{request.user.first_name} messaged you!",
        )
        return redirect('chat_detail', username=receiver_username)
    
class StartChatView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        receiver_username = request.POST.get('receiver')
        if not receiver_username:
            # Handle case where no user is selected
            return redirect('chat_list')
        return redirect('chat_detail', username=receiver_username)  