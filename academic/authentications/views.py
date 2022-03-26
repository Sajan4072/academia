from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .auth import unauthenticated_user
from .forms import CreateUserForm
from .models import Profile


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser and user.is_staff:
                return redirect('/admins')
            elif not user.is_superuser and not user.is_staff:
                return redirect('/students')
            elif not user.is_superuser and user.is_staff:
                return redirect('/lecturers')
        elif user is None:
            messages.add_message(request, messages.ERROR, 'Please provide correct credentials')
    return render(request, 'authentications/login.html')


@login_required
def signout(request):
    logout(request)
    return redirect('/auth/login_page')
