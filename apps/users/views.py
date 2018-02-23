from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

def index(request):
    request.session['loggedin']= False
    return render(request, 'users/index.html')

def secrets(request):
    if request.session['loggedin']!=True:
        return redirect('users:index')
    else:
        return render(request, 'users/secrets.html', {'secrets': Secret.objects.order_by('secret')[:10]}, {'user': User.objects.get(id = request.session['user_id'])})
def popular(request):
    if request.session['loggedin']!= True:
        return redirect('users:index')
    else:
        return render(request, 'users/popular_secrets.html', {'secrets': Secret.objects.order_by('secret')[:5]})

def add(request):
    userSecret_id = request.session['user_id']
    User.objects.add_secret(request.POST, userSecret_id)
    return redirect('users:secrets')

def create(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)
            return redirect('/')
        else:
            request.session['loggedin']=True
            user = User.objects.register(request.POST)
            request.session['first_name'] = user.first_name
            request.session['user_id'] = user.id
            return redirect('users:secrets')

def login(request):
    if request.method == 'POST':
        errors = User.objects.validate_login(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)
            return redirect('/')
        else:
            request.session['loggedin']=True
            user = User.objects.login(request.POST)
            request.session['first_name'] = user.first_name
            request.session['user_id'] = user.id
            return redirect('users:secrets')

def like(request, id):
    userSecret_id = request.session['user_id']
    User.objects.add_like(request.POST, id, userSecret_id)
    return redirect('users:secrets')

def logout(request):
    request.session.clear()
    return redirect('/')