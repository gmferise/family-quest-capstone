from django.db import models
from familystructure.fields import ListAsStringField

from django.utils.translation import ugettext_lazy as _

class Person(models.Model):
    """
    | Field           | Details             |
    | :-------------- | :------------------ |
    | first_name      | 32 chars            |
    | nickname        | 32 chars, optional  |
    | middle_name     | 32 chars, optional  |
    | last_name       | 32 chars            |
    | title           | 16 chars, optional  |
    | tagline         | 64 chars, optional  |
    | birth_date      | Date                |
    | death_date      | Date, optional      |
    | profile_picture | ImageField          |
    | is_claimed      | bool, default False |
    | facts           | ListAsStringField   |
    """

    class Meta:
        verbose_name_plural = _('people')

    first_name = models.CharField(
        _('first name'),
        max_length=32,
    )
    
    nickname = models.CharField(
        _('nickname'),
        max_length=32,
        blank=True,
        null=True,
    )
    
    middle_name = models.CharField(
        _('middle name'),
        max_length=32,
        blank=True,
        null=True,
    )
    
    last_name = models.CharField(
        _('last name'),
        max_length=32,
    )
    
    title = models.CharField(
        _('title'),
        max_length=16,
        blank=True,
        null=True,
    )
    
    tagline = models.CharField(
        _('tagline'),
        max_length=64,
        blank=True,
        null=True,
    )
    
    birth_date = models.DateField(
        _('birth date'),
        auto_now=False,
        auto_now_add=False,
    )
    
    death_date = models.DateField(
        _('death date'),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    profile_photo = models.ImageField(
        _('profile photo'),
        # MEDIA_ROOT/profile_photos/ == website/static/uploads/profile_photos/
        upload_to='profile_photos/',
        null=True,
        blank=True,
    )
    
    is_claimed = models.BooleanField(
        _('is claimed'),
        default=False,
    )
    
    facts = ListAsStringField(default=[], blank=True, null=True)

    def __str__(self):
        middle = ''
        end = f' {self.title}' if self.title else ''
        if self.nickname:
            middle += f' "{self.nickname}"'
        if self.middle_name:
            middle += f' {self.middle_name}'
        return f'{self.first_name}{middle} {self.last_name}{end}'


class Relation(models.Model):
    """
    | Field       | Details             |
    | :---------- | :------------------ |
    | source      | fk Person           |
    | target      | fk Person           |
    | is_upward   | bool                |
    """
    source = models.ForeignKey(
        'familystructure.Person',
        verbose_name=_('source person'),
        related_name='relations_out',
        on_delete=models.CASCADE,
    )
    target = models.ForeignKey(
        'familystructure.Person',
        verbose_name=_('target person'),
        related_name='relations_in',
        on_delete=models.CASCADE,
    )
    is_upward = models.BooleanField(
        _('is upward'),
        default=True,
    )

    def __str__(self):
        if self.is_upward:
            return f'{self.target} -> {self.source}'
        return f'{self.source} -- {self.target}'

class FamilyCircle(models.Model):
    """
    | Field       | Details             |
    | :---------- | :------------------ |
    | name        | 64 chars            |
    | members     | mtm Person          |
    | managers    | mtm UserAccount     |
    """
    name = models.CharField(_('name'), max_length=64)
    members = models.ManyToManyField(
        'familystructure.Person',
        verbose_name=_('members'),
        related_name='family_circles',
    )
    managers = models.ManyToManyField(
        'useraccount.UserAccount',
        verbose_name=_('managers'),
        related_name='family_circles_managing',
    )

    def __str__(self):
        return f'{self.name} ({len(self.members.all())} members)'