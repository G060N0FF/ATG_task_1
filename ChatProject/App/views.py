from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import SearchForm, PictureForm, ChatGroupForm, FindGroupForm
from .models import Message, ChatGroup, Notification
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

    # a form to create a group
    group_create_form = ChatGroupForm()

    # a form to search for groups
    find_group_form = FindGroupForm()

    found_users = []
    found_groups = []

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

        # check if the user has created a group
        elif 'name' in request.POST:
            group_create_form = ChatGroupForm(request.POST)
            if group_create_form.is_valid():
                name = request.POST['name']
                new_group = ChatGroup(name=name)
                new_group.save()
                new_group.users.add(request.user)
                new_group.save()

        # check if the user is searching for groups
        elif 'gr_name' in request.POST:
            find_group_form = FindGroupForm(request.POST)
            if find_group_form.is_valid():
                gr_name = request.POST['gr_name']
                found_groups = ChatGroup.objects.filter(name__icontains=gr_name)

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
        'found_users': found_users,
        'group_create_form': group_create_form,
        'find_group_form': find_group_form,
        'found_groups': found_groups,
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
    context = {'room': room, 'user': request.user}
    return render(request, 'App/chat.html', context)


# preload messages
@login_required
def load_messages(request):
    room = request.GET.get('room', None)

    messages = [[msg.user.username, msg.text, str(msg.date_time).split('.')[0], msg.pk, msg.image.url] if msg.image else [msg.user.username, msg.text, str(msg.date_time).split('.')[0], msg.pk] for msg in Message.objects.filter(group=room)]

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

    return redirect(f'/chat/{new_url}/')


# delete message
@login_required
def delete_message(request):
    id = request.GET.get('id', None)

    Message.objects.get(pk=id).delete()

    return JsonResponse({})


# check online status
@login_required
def check_status(request):
    id = request.GET.get('id', None)

    return JsonResponse(
        {
            'data': {'is_online': User.objects.get(pk=id).profile.is_online, 'name': User.objects.get(pk=id).username}
        }
    )


@login_required
# a view to see group options
def group(request, group_id):
    group = ChatGroup.objects.get(pk=group_id)

    # security check
    if request.user not in group.users.all():
        return redirect('/')

    user_search_form = SearchForm()
    found_users = []

    if request.method == 'POST':
        user_search_form = SearchForm(request.POST)
        if user_search_form.is_valid():
            query = request.POST['query']
            found_users = User.objects.filter(username__icontains=query)

    context = {'group': group, 'user_search_form': user_search_form, 'found_users': found_users}
    return render(request, 'App/group.html', context)


@login_required
# a view to add group members
def add_to_group(request, group_id, user_id):
    group = ChatGroup.objects.get(pk=group_id)

    # security check
    if request.user not in group.users.all():
        return redirect('/')

    group.users.add(User.objects.get(pk=user_id))
    group.save()

    return redirect('/group/'+str(group.pk))


@login_required
# a function to leave a group
def leave_group(request, group_id):
    group = ChatGroup.objects.get(pk=group_id)

    # security check
    if request.user not in group.users.all():
        return redirect('/')

    group.users.remove(request.user)

    return redirect('/group/'+str(group.pk))


@login_required
# a function to join a group
def join_group(request, group_id):
    group = ChatGroup.objects.get(pk=group_id)

    group.users.add(request.user)
    group.save()

    return redirect('/group/' + str(group.pk))


@login_required
def notifications(request):
    notis = request.user.notifications.all()

    context = {'notis': notis}
    return render(request, 'App/notifications.html', context)
