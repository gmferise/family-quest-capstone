from re import search as re_search
from django.db.models import Count
from django.db.models.expressions import OuterRef, Subquery
from website.base_views import BaseEndpoint
from socialmedia.models import (
    Chat,
    Message,
    MessageNotification,
    CommentNotification,
)
from familystructure.models import (
    FamilyCircle,
)
from useraccount.models import UserAccount

from json import (
    loads as hydrate_json,
)

class ChatsEndpoint(BaseEndpoint):
    
    def get(self, request):
        """Get all chats for this user"""

        chats = (
            Chat.objects
                .filter(members=request.user)
                .annotate(messages_count=Count('messages'))
                .exclude(messages_count__lt=1)
                .annotate(last_message_at=Subquery(
                    Message.objects.filter(
                        chat=OuterRef('pk'),
                    ).order_by('-sent_at')
                    .values('sent_at')[:1]
                ))
                .order_by('-last_message_at')
        )
        json_chats = []
        for chat in chats:
            members = chat.members.all()
            not_me = members.exclude(id=request.user.id)
            shared_circles = []
            if all(bool(m.person) for m in members):
                shared_circles = [
                    circle.name for circle in
                    FamilyCircle.objects.filter(members__in=[m.person for m in members]).distinct()
                ]
            last_message = chat.messages.order_by('-sent_at').first()
            json_chats.append({
                'id': chat.id,
                'latestmessage': {
                    'content': last_message.content,
                    'sent_at': last_message.sent_at,
                },
                'members': [str(m) for m in not_me],
                'circles': shared_circles,
            })
        return self.ok(request, { 'chats': json_chats })
    
    def post(self, request):
        """
        Start a new chat

        Request Body:
        ```javascript
        {
            'members': [ UserAccount.id ],
            'message': String,
        }
        ```
        """
        json = hydrate_json(request.body)

        chat = Chat.objects.create()
        member_ids = { request.user.id } | set(
            int(user_id) for user_id in json['members']
        )
        chat.members.set(UserAccount.objects.filter(id__in=list(member_ids)))

        message = Message.objects.create(
            content=json['message'],
            author=request.user,
            chat=chat,
        )
        for user in chat.members.all():
            if user != request.user:
                MessageNotification.objects.create(
                    target_user=user,
                    target_message=message,
                )

        return self.get(request)



class ChatDetailEndpoint(BaseEndpoint):

    def get(self, request, chat_id):
        """Get all messages in this chat"""
        try:
            chat = Chat.objects.get(id=chat_id)        
            if request.user not in chat.members.all():
                return self.no_perms()
            return self.ok(request, chat.json_serialize())
        except Chat.DoesNotExist:
            return self.not_found()
    
    def post(self, request, chat_id):
        """
        Send a new message to this chat, making the necessary notifications
        Needs `X-CSRFToken` header set

        Request Body:
        ```javascript
        {
            'content': String,
        }
        ```
        """
        json = hydrate_json(request.body)
        try:
            chat = Chat.objects.get(id=chat_id)
            members = chat.members.all()
            if request.user not in members:
                return self.no_perms()
            
            message = Message.objects.create(
                content=json['content'],
                author=request.user,
                chat=chat,
            )
            for user in members:
                if user != request.user:
                    MessageNotification.objects.create(
                        target_user=user,
                        target_message=message,
                    )
            return self.done(request, chat.json_serialize())
        except Chat.DoesNotExist:
            return self.not_found()
        except KeyError:
            return self.not_ok()

class NotifsEndpoint(BaseEndpoint):
    
    def get(self, request):
        """Get all of the current user's notifications"""
        messages = MessageNotification.objects.filter(target_user=request.user)
        comments = CommentNotification.objects.filter(target_user=request.user)
        return self.ok(request, {
            'notifs': sorted(
                [ m.json_serialize() for m in messages ]
                + [ c.json_serialize() for c in comments ],
                key=lambda n: n['created_at'],
                reverse=True,
            )
        })
    
    def delete(self, request):
        """Clear all of the current user's notifications"""
        MessageNotification.objects.filter(target_user=request.user).delete()
        CommentNotification.objects.filter(target_user=request.user).delete()
        return self.get(request)

class NotifsDetailEndpoint(BaseEndpoint):
    
    def delete(self, request, notif_slug):
        try:
            match = re_search(r'^([a-z]+)\-([0-9]+)$', notif_slug)
            if match is None:
                return self.not_ok()
            
            model, model_id = match.groups()
            model_id = int(model_id)

            if model == 'message':
                notif = MessageNotification.objects.get(id=model_id)
            elif model == 'comment':
                notif = CommentNotification.objects.get(id=model_id)
            
            if request.user == notif.target_user:
                notif.delete()
            else:
                return self.no_perms()

            messages = MessageNotification.objects.filter(target_user=request.user)
            comments = CommentNotification.objects.filter(target_user=request.user)
            return self.ok(request, {
                'notifs': sorted(
                    [ m.json_serialize() for m in messages ]
                    + [ c.json_serialize() for c in comments ],
                    key=lambda n: n['created_at'],
                    reverse=True,
                )
            })
        except MessageNotification.DoesNotExist:
            return self.not_found()
        except CommentNotification.DoesNotExist:
            return self.not_found()