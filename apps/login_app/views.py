from django.shortcuts import render, redirect
from models import User 
from django.contrib import messages

def index(request):

    return render(request, 'login_app/index.html')

def register(request):

    results = User.objects.validate(request.POST)
    if results['status'] == True:
        user = User.objects.creator(request.POST)
        messages.success(request, 'New account has been created.')
        messages.success(request, 'Please sign in.')
    else:
        for error in results['errors']:
            messages.error(request, error)
    return redirect('/')

def login(request):

    results = User.objects.loginVal(request.POST)
    if results['status'] == False:
        messages.error(request, "Incorrect email or password. Please try again.")
        return redirect('/')
    request.session['email'] = results['user'].email
    request.session['alias'] = results['user'].alias
    request.session['user_id'] = results['user'].id
    return redirect('/poke/')

def logout(request):

    messages.error(request, "You are now signed out.")
    request.session.flush()
    #messages.error(request, "Definitely you are signed out.")
    return redirect('/')
