from django.shortcuts import render, redirect
from ..login_app.models import User
from models import Poke

def dashboard(request):

    if 'email' not in request.session:
        return redirect('/')
    cur_user = User.objects.get(id= request.session['user_id'])
    cur_user.r_count = cur_user.got.count()
    cur_user.g_count = cur_user.gave.count()
    pokers = User.objects.exclude(id=request.session['user_id'])
    for i in pokers:
        i.count = i.got.count()
    context = {
        'cur_user': cur_user,
        'pokers': pokers,     
    }
    return render(request, 'poke_app/dashboard.html', context)

def add(request, id):

    if 'email' not in request.session:
        return redirect('/')
    Poke.objects.create(giver = User.objects.get(id=request.session['user_id']), receiver = User.objects.get(id = id))
    cur_user = User.objects.get(id= request.session['user_id'])
    cur_user.r_count = cur_user.got.count()
    cur_user.g_count = cur_user.gave.count()
    pokers = User.objects.exclude(id=request.session['user_id'])
    for i in pokers:
        i.count = i.got.count()
    context = {
        'cur_user': cur_user,
        'pokers': pokers,
    }
    return render(request, 'poke_app/dashboard.html', context)
