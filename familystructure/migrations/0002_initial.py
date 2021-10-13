# Generated by Django 3.2.7 on 2021-10-12 16:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('familystructure', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='familycircle',
            name='managers',
            field=models.ManyToManyField(related_name='family_circles_managing', to=settings.AUTH_USER_MODEL, verbose_name='managers'),
        ),
        migrations.AddField(
            model_name='familycircle',
            name='members',
            field=models.ManyToManyField(related_name='family_circles', to='familystructure.Person', verbose_name='members'),
        ),
    ]