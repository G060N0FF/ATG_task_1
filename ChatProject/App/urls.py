from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # home page
    path('', views.index, name='index'),
    # accounts path
    path('accounts/', include('django.contrib.auth.urls')),
    # registration path
    path('register/', views.register, name='register'),
    # chat url
    path('chat/<path:room>/', views.chat, name='chat'),
    # load messages when a user joins the chat lobby
    path('load_messages/', views.load_messages, name='load_messages'),
    # create a url for two users to chat
    path('create_url/<path:second_id>/', views.create_url, name='create_url'),
    # a path do delete a message from the database
    path('delete_message/', views.delete_message, name='delete_message'),
    # a path to check the active status of a user
    path('check_status/', views.check_status, name='check_status'),
    # a path to see group options
    path('group/<path:group_id>', views.group, name='group'),
    # a path to add users to the group
    path('add_to_group/<path:group_id>/<path:user_id>/', views.add_to_group, name='add_to_group'),
    # a path to leave the group
    path('leave_group/<path:group_id>/', views.leave_group, name='leave_group'),
    # a path to join a group
    path('join_group/<path:group_id>/', views.join_group, name='join_group'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
