# Generated by Django 3.2.7 on 2021-10-07 22:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction_type', models.CharField(choices=[('', 'Default'), ('heart', 'Heart'), ('smiley', 'Smiley'), ('thumbs_up', 'Thumbs_up')], default='', max_length=12)),
                ('post_reaction', models.ManyToManyField(blank=True, related_name='post_reaction', to='socialmedia.Post')),
            ],
        ),
        migrations.CreateModel(
            name='CommentNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_inform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_inform', to=settings.AUTH_USER_MODEL)),
                ('post_notify', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_notify', to='socialmedia.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=140)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('post_comment_added', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_comment_added', to='socialmedia.post')),
            ],
        ),
    ]
