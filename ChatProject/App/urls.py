from django.urls import path, include
from . import views

urlpatterns = [
    # home page
    path('', views.index, name='index'),
    # accounts path
    path('accounts/', include('django.contrib.auth.urls')),
    # registration path
    path('register/', views.register, name='register'),
    # chat url
    path('chat/', views.chat, name='chat'),
    # load messages when a user joins the chat lobby
    path('load_messages/', views.load_messages, name='load_messages')
]
