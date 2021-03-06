# Generated by Django 3.2.7 on 2021-10-12 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('familystructure', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialmedia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_made', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AddField(
            model_name='post',
            name='family_circle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='familystructure.familycircle', verbose_name='family circle'),
        ),
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_made', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AddField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='socialmedia.chat', verbose_name='chat'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_made', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='commented_on',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='socialmedia.post'),
        ),
        migrations.AddField(
            model_name='chat',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='members'),
        ),
        migrations.AddField(
            model_name='basereaction',
            name='reactor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postreaction',
            name='target_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='socialmedia.post'),
        ),
        migrations.AddField(
            model_name='messagenotification',
            name='target_message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_created', to='socialmedia.message'),
        ),
        migrations.AddField(
            model_name='messagenotification',
            name='target_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_notifs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentreaction',
            name='target_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='socialmedia.comment'),
        ),
        migrations.AddField(
            model_name='commentnotification',
            name='target_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_created', to='socialmedia.comment'),
        ),
        migrations.AddField(
            model_name='commentnotification',
            name='target_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_notifs', to=settings.AUTH_USER_MODEL),
        ),
    ]
