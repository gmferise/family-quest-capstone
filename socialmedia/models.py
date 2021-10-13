from django.db import models
from socialmedia.base_models import BaseReaction, BaseNotification
from django.urls import reverse

from django.utils.translation import ugettext_lazy as _

class Post(models.Model):
    """
    | Field         | Details         |
    | :------------ | :-------------- |
    | title         | 50 chars        |
    | content       | TextField       |
    | post_photo    | ImageField      |
    | created_at    | DateTime        |
    | author        | fk UserAccount  |
    | family_circle | fk FamilyCircle |
    """
    title = models.CharField(max_length=50)
    content = models.TextField(
        null=True,
        blank=True,
    )
    post_photo = models.ImageField(
        _('post photo'),
        # MEDIA_ROOT/post_photos/ == website/static/uploads/post_photos/
        upload_to='post_photos/',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        'useraccount.UserAccount',
        verbose_name=_('author'),
        related_name='posts_made',
        on_delete=models.CASCADE,
    )
    family_circle = models.ForeignKey(
        'familystructure.FamilyCircle',
        verbose_name=_('family circle'),
        related_name='posts',
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    """
    | Field        | Details        |
    | :----------- | :------------- |
    | body         | TextField      |
    | created_at   | DateTime       |
    | author       | fk UserAccount |
    | commented_on | fk Post        |
    """
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        'useraccount.UserAccount',
        related_name='comments_made',
        on_delete=models.CASCADE,
        null=True,
    )
    commented_on = models.ForeignKey(
        'socialmedia.Post',
        related_name='comments',
        on_delete=models.CASCADE,
        blank=True,
    )

    def __str__(self):
        return self.body

class PostReaction(BaseReaction):
    """
    | Field         | Details                   |
    | :------------ | :------------------------ |
    | reaction_type | PostReaction.ReactionType |
    | reactor       | fk UserAccount            |
    | target_post   | fk Post                   |

    `ReactionType`:
    `HEART`
    `SMILEY`
    `THUMBS_UP`
    """
    TARGET_MODEL = 'socialmedia.Post'
    target_post = models.ForeignKey(
        TARGET_MODEL,
        related_name='reactions',
        on_delete=models.CASCADE,
    )

class CommentReaction(BaseReaction):
    """
    | Field            | Details              |
    | :--------------- | :------------------- |
    | reaction_type    | Comment.ReactionType |
    | reactor          | fk UserAccount       |
    | target_comment   | fk Comment           |

    `ReactionType`:
    `HEART`
    `SMILEY`
    `THUMBS_UP`
    """
    TARGET_MODEL = 'socialmedia.Comment'
    target_comment = models.ForeignKey(
        TARGET_MODEL,
        related_name='reactions',
        on_delete=models.CASCADE,
    )

class CommentNotification(BaseNotification):
    """
    | Field          | Details         |
    | :------------- | :-------------- |
    | target_user    | fk UserAccount  |
    | target_comment | fk Comment      |
    """
    TARGET_MODEL = 'socialmedia.Comment'
    target_comment = models.ForeignKey(
        TARGET_MODEL,
        related_name='notifications_created',
        on_delete=models.CASCADE,
    )
    target_user = models.ForeignKey(
        'useraccount.UserAccount',
        related_name='comment_notifs',
        on_delete=models.CASCADE,
    )

    def json_serialize(self):
        return {
            'slug': f'comment-{self.id}',
            'type': 'comment',
            'from': str(self.target_comment.author),
            'created_at': self.created_at,
            'url': f"reverse('comment detail view name or post detail view name with hash, fixme when one exists', {self.target_comment.id})",
        }
    
    def __str__(self):
        return f'Comment notif for {self.target_user} from {self.target_comment.author}'

class MessageNotification(BaseNotification):
    """
    | Field          | Details         |
    | :------------- | :-------------- |
    | target_user    | fk UserAccount  |
    | target_message | fk Message      |
    """
    TARGET_MODEL = 'socialmedia.Message'
    target_message = models.ForeignKey(
        TARGET_MODEL,
        related_name='notifications_created',
        on_delete=models.CASCADE,
    )
    target_user = models.ForeignKey(
        'useraccount.UserAccount',
        related_name='message_notifs',
        on_delete=models.CASCADE,
    )

    def json_serialize(self):
        return {
            'slug': f'message-{self.id}',
            'type': 'message',
            'from': str(self.target_message.author),
            'created_at': self.created_at,
            'url': reverse('chat', args=[self.target_message.chat.id]),
        }
    
    def __str__(self):
        return f'Post notif for {self.target_user} from {self.target_message.author}'

class Chat(models.Model):
    """
    | Field    | Details         |
    | :------- | :-------------- |
    | members  | mtm UserAccount |
    """
    members = models.ManyToManyField(
        'useraccount.UserAccount',
        verbose_name=_('members'),
    )

    def __str__(self):
        return f"{' + '.join(str(u) for u in self.members.all())} ({len(self.messages.all())} messages)"
    
    def json_serialize(self):
        return {
            'messages': [
                message.json_serialize()
                for message in self.messages.all()
            ],
        }

class Message(models.Model):
    """
    | Field    | Details         |
    | :------- | :-------------- |
    | content  | Textfield       |
    | sent_at  | DateTime        |
    | author   | fk UserAccount  |
    | chat     | fk Chat         |
    """
    content = models.TextField(
        _('content'),
        null=False,
        blank=False,
    )

    sent_at = models.DateTimeField(
        _('sent_at'),
        auto_now_add=True,
    )

    author = models.ForeignKey(
        'useraccount.UserAccount',
        verbose_name=_('author'),
        related_name='messages_made',
        on_delete=models.CASCADE,
    )

    chat = models.ForeignKey(
        'socialmedia.Chat',
        verbose_name=_('chat'),
        related_name='messages',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'[{self.sent_at.ctime()}] {self.author}: {self.content}'
    
    def json_serialize(self):
        return {
            'message_id': self.id,
            'content': self.content,
            'sent_at': self.sent_at,
            'author': self.author.json_serialize(),
        }
