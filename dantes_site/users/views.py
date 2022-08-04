from django.http import HttpResponseRedirect, HttpRequest
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm, UserAuthenticationForm


def register_view(request: HttpRequest):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('index')  # TODO: Add verification page
        else:
            context['form'] = form
    elif request.method == 'GET':
        context['form'] = UserRegistrationForm()
    return render(request, 'users/register.html', context)


def logout_view(request: HttpRequest):
    logout(request)
    return redirect('index')


def login_view(request: HttpRequest):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('index')
        context['form'] = form
    elif request.method == 'GET':
        context['form'] = UserAuthenticationForm()
    return render(request, 'users/login.html', context)


@login_required
def account_view(request: HttpRequest):
    return render(request, 'users/account.html')
