from django.db import models
from django.utils.translation import ugettext_lazy as _

class BaseNotification(models.Model):
    """
    To extend, add a TARGET_MODEL and target FK field
    ```
    TARGET_MODEL = 'app.?'
    target_? = models.ForeignKey(
        TARGET_MODEL,
        related_name='notifications_created',
        on_delete=models.CASCADE,
    )
    target_user = models.ForeignKey(
        'useraccount.UserAccount',
        related_name='???',
        on_delete=models.CASCADE,
    )
    ```
    """

    created_at = models.DateTimeField(
        _('created_at'),
        auto_now_add=True,
    )

class BaseReaction(models.Model):
    """
    To extend, add a TARGET_MODEL and target FK field
    ```
    TARGET_MODEL = 'app.?'
    target_? = models.ForeignKey(
        TARGET_MODEL,
        related_name='?_reactions',
        on_delete=models.CASCADE,
    )
    ```
    """

    class ReactionType(models.TextChoices):
            HEART = 'heart', _('Heart'),
            SMILEY = 'smiley', _('Smiley'),
            THUMBS_UP = 'thumbs_up', _('Thumbs_up')

    reaction_type = models.CharField(
        max_length=12,
        choices=ReactionType.choices,
        default=ReactionType.THUMBS_UP,
    )
    reactor = models.ForeignKey(
        'useraccount.UserAccount',
        related_name='reactor',
        on_delete=models.CASCADE,
    )
    

    def __str__(self):
        t = self.TARGET_MODEL.split('.')[1]
        return f'{self.reactor.person} reacted to a {t} with a {self.reaction_type}'