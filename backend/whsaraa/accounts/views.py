from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme


def login_view(request):
    error = ''
    next_url = request.POST.get('next') or request.GET.get('next') or ''

    if request.method == 'POST':
        username = request.POST.get('userId', '').strip()
        password = request.POST.get('userPass', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('home')
        else:
            error = 'نام کاربری یا گذرواژه اشتباه است.'

    return render(request, 'login.html', {'error': error, 'next': next_url})


def logout_view(request):
    logout(request)
    return redirect('home')