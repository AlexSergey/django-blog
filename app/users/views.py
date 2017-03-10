from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from .forms import UserLoginForm, UserRegisterForm

def login_view(request):
    # if we redirected when we was not auth user
    # we will be redirect to login
    # with ?next parameter
    # it need for after login we will be redirect to this "next" url
    next = request.GET.get('next')
    title = 'Login'
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    return render(request, 'account_form.html', {
        'form': form,
        'title': title
    })

def register_view(request):
    next = request.GET.get('next')
    title = 'Register'
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'title': title,
        'form': form
    }

    return render(request, 'account_form.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')