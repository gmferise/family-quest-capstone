"""webconfig URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website import views as frontend

from socialmedia.views import (
    ChatsEndpoint,
    ChatDetailEndpoint,
    NotifsEndpoint,
    NotifsDetailEndpoint,
)

from useraccount.views import (
    UserSearchEndpoint,
)

from familystructure.views import (
    PersonSearchEndpoint,
)

urlpatterns = [
    # Endpoints
    path('api/chats/', ChatsEndpoint.as_view()),
    path('api/chat/<int:chat_id>/', ChatDetailEndpoint.as_view()),
    path('api/notifs/', NotifsEndpoint.as_view()),
    path('api/notifs/<slug:notif_slug>/', NotifsDetailEndpoint.as_view()),
    path('api/user/search/', UserSearchEndpoint.as_view()),
    path('api/person/search/', PersonSearchEndpoint.as_view()),
    
    # Views
    path('', frontend.Home.as_view(), name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('logout/', frontend.Logout.as_view(), name='logout'),
    path('signup/', frontend.Signup.as_view(), name='signup'),
    path('signup/about-you/', frontend.SignupPerson.as_view(), name='claim_person'),
    path('login/', frontend.Login.as_view(), name='login'),
    path('person/<int:person_id>/', frontend.PersonDetail.as_view(), name='person_detail'),
    path('person/<int:person_id>/edit/', frontend.PersonEdit.as_view(), name='person_edit'),
    path('person/<int:person_id>/add/spouse/', frontend.PersonAddSpouse.as_view(), name='person_add_spouse'),
    path('person/<int:person_id>/add/parent/', frontend.PersonAddParent.as_view(), name='person_add_parent'),
    path('circles/', frontend.FamilyCircles.as_view(), name='circle_list'),
    path('circle/<int:circle_id>/', frontend.FamilyCircleDetail.as_view(), name='circle_detail'),
    path('circle/<int:circle_id>/manage/', frontend.FamilyCircleManage.as_view(), name='circle_manage'),
    path('circle/new/', frontend.CreateFamilyCircle.as_view(), name='create_circle'), # TODO: switch view
    path('circle/<int:circle_id>/add/person/', frontend.FamilyCircleAddPerson.as_view(), name='circle_add_person'),
    path('circle/<int:circle_id>/add/post/', frontend.CreatePost.as_view(), name='create_post'),
    path('post/<int:post_id>/', frontend.PostDetail.as_view(), name='post_detail'),
    path('settings/', frontend.UserEdit.as_view(), name='user_edit'),
    path('chats/', frontend.AllChats.as_view(), name='chats'),
    path('chat/<int:chat_id>/', frontend.SingleChat.as_view(), name='chat'),
    path('user/<int:user_id>/', frontend.Home.as_view(), name='user_detail'),
    path('familynavigator/<int:person_id>/', frontend.FamilyNavigator.as_view(), name='family_navigator')
]

