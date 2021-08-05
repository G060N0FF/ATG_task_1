from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import SearchForm, PictureForm
from .models import Message
from django.http import JsonResponse


# index view
@login_required
def index(request):
    # a form to update the user information
    user_change_form = UserCreationForm()

    # a form to search for users
    user_search_form = SearchForm()

    # a form to change the profile picture
    pfp_form = PictureForm()

    found_users = []

    # if a form has been filled
    if request.method == 'POST':
        # check if the user has been changed
        if 'username' in request.POST:
            user_change_form = UserCreationForm(data=request.POST, instance=request.user)
            if user_change_form.is_valid():
                username = request.POST['username']
                password = request.POST['password1']
                if not User.objects.filter(username=username).exists():
                    request.user.username = username;
                    request.user.set_password(password)
                    request.user.save()

                    login(request, request.user)

        # check if the user has searched for other users
        elif 'query' in request.POST:
            user_search_form = SearchForm(request.POST)
            if user_search_form.is_valid():
                query = request.POST['query']
                found_users = User.objects.filter(username__icontains=query)

        # check if the user has changed his/her profile picture
        else:
            pfp_form = PictureForm(request.POST, request.FILES)
            if pfp_form.is_valid():
                request.user.profile.profile_picture = request.FILES['picture']
                request.user.profile.save()

    context = {
        'user': request.user,
        'user_change_form': user_change_form,
        'user_search_form': user_search_form,
        'pfp_form': pfp_form,
        'found_users': found_users
    }
    return render(request, 'App/index.html', context)


# registration path
def register(request):
    form = UserCreationForm()

    # if the form has been filled
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            # retrieve the username and the password
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # create a User instance
            user = authenticate(request, username=username, password=password)
            login(request, user)

            return redirect('/')

    context = {'form': form}
    return render(request, 'registration/register.html', context)


# chat view
@login_required
def chat(request, room):
    context = {'room': room}
    return render(request, 'App/chat.html', context)


# preload messages
@login_required
def load_messages(request):
    messages = [{'username': msg.user.username, 'text': msg.text} for msg in Message.objects.all()]

    return JsonResponse(
        {
            'data': messages,
        }
    )


@login_required
def create_url(request, second_id):
    curr_id = str(request.user.pk)
    second_id = str(second_id)

    new_url = max(curr_id, second_id) + '-' + min(curr_id, second_id)

    return redirect('/chat/new_url/')
