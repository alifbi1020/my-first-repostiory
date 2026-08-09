from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('userId', '').strip()
        password = request.POST.get('userPass', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'نام کاربری یا گذرواژه اشتباه است.'

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')