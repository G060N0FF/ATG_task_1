from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


# index view
@login_required
def index(request):
    # a form to update the user information
    user_change_form = UserCreationForm()

    user_copy = request.user.username

    # if a form has been filled
    if request.method == 'POST':
        # get the filled form
        user_change_form = UserCreationForm(data=request.POST, instance=request.user)

        # check if the user has been changed
        if user_change_form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            if not User.objects.filter(username=username).exists():
                request.user.username = username;
                request.user.set_password(password)
                request.user.save()

                login(request, request.user)

            return redirect('/')
        else:
            request.user.username = user_copy
            request.user.save()

    context = {'user': request.user.username, 'user_change_form': user_change_form}
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
