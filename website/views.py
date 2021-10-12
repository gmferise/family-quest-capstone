from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from useraccount.forms import LoginForm, SignupForm
from useraccount.models import UserAccount

from django.views.generic import View
from website.base_views import GenericFormView

from socialmedia.models import Chat

from functools import reduce

class Home(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'index.html')

class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('home')

class Login(GenericFormView):
    FormClass = LoginForm
    template_text = {"header":"Log In to Family Quest", "submit":"Log In"}

    def _handle_submission(self, request, form):
        user = authenticate(request, email=form.get('email'), password=form.get('password'))
        if user:
            login(request, user)
            return redirect('home')

class Signup(GenericFormView):
    FormClass = SignupForm
    template_text = {"header":"Sign Up to Family Quest", "submit":"Get Started"}

    def _handle_submission(self, request, form):
        UserAccount.objects.create_user(
            email=form.get('email'),
            password=form.get('password'),
        )
        user = authenticate(request,
            email=form.get('email'),
            password=form.get('password')
        )
        if user:
            login(request,user)
            return redirect('home')

class AllChats(LoginRequiredMixin, View):
    
    def get(self, request):
        chatobjs = Chat.objects.filter(members__in=[request.user])
        chats = []
        # include only chats that have at least 1 message
        for chat in [c for c in chatobjs if c.messages.count() > 1]:
            circles = []
            members = chat.members.all()
            # if all members in a chat have people, find the intersection of their family circles
            if all([bool(m.person) for m in members]):
                circles = [set(m.person.family_circles.all()) for m in members]
                circles = reduce(lambda a, b: a & b, circles)
            # serialize chat to object for template
            chats.append({
                "id":chat.id,
                "latestmessage":chat.messages.order_by('sent_at').last(),
                "members":", ".join([str(m) for m in chat.members.exclude(id=request.user.id)]),
                "circles": circles
            })
        # sort by latest message date first
        chats = reversed(sorted(chats, key=lambda x: x['latestmessage'].sent_at.isoformat()))
        return render(request, 'chats.html', {"chats":chats})

class SingleChat(LoginRequiredMixin, View):

    def get(self, request, chat_id):
        return render(request, 'chat.html', {"chat":Chat.objects.get(chat_id)})