from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.urls import reverse

from unicodedata import normalize

from useraccount.manager import UserAccountManager

from django.utils.translation import ugettext_lazy as _

class UserAccount(AbstractBaseUser, PermissionsMixin):
    """
    | Field    | Details    |
    | :------- | :--------- |
    | email    | unique     |
    | password | 128 chars  |
    | person   | oto Person | # TODO: ADD THIS
    """

    username_validator = EmailValidator()

    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=False,
        error_messages={
            'unique': _('That email is already in use.'),
        },
    )

    person = models.OneToOneField(
        'familystructure.Person',
        verbose_name=_('person'),
        related_name='useraccount',
        null=True,
        on_delete=models.DO_NOTHING,
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserAccountManager()

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    class Meta:
        verbose_name = _('useraccount')
        verbose_name_plural = _('useraccounts')

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return str(self.person) if self.person else self.email
    
    @classmethod
    def normalize_email(cls, email):
        return normalize('NFKC', email) if isinstance(email, str) else email
    
    def json_serialize(self):
        if self.person:
            return {
                'account_id': self.id,
                'person_id': self.person.id,
                'email': self.email,
                'profile_url': reverse('user_detail', args=[self.id]),
                'photo_url': f'/static/uploads{self.profile_photo.url}',
                'name': str(self.person),
                'tagline': self.person.tagline,
            }
        return {
            'account_id': self.id,
            'email': self.email,
            'profile_url': reverse('user_detail', args=[self.id]),
            'photo_url': f'/static/images/default.png',
        }