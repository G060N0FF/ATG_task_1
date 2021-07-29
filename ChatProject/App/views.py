from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


# index view
@login_required
def index(request):
    context = {}
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

            # validate data
            pass

            # create a User instance
            user = authenticate(request, username=username, password=password)
            login(request, user)

        return redirect('/')

    context = {'form': form}
    return render(request, 'registration/register.html', context)
