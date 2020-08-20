from django.shortcuts import redirect, render
from django.contrib import messages
import bcrypt
from .models import User, Message, Comment

def index(request):
    return render(request, 'index.html')


def success(request):
   
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session["user_id"]),
        'all_messages': Message.objects.all(),
        'all_comments': Comment.objects.all(),
    }

    return render(request, 'wall.html', context)



def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        hash_browns = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_browns,
        )     
        request.session['user_id'] = user.id
        return redirect('/wall')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_to_login = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user_to_login.id 
        return redirect('/wall')

def logout(request):
    request.session.flush()
    return redirect('/')


def post_message(request):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    Message.objects.create(
        message = request.POST['message'],
        user = logged_in_user,
    )
    return redirect('/wall')

def post_comment(request):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    Comment.objects.create(
        comment = request.POST['comment'],
        user = logged_in_user,
        message = Message.objects.get(id=request.POST['msg_id'])
    ),


    return redirect('/wall')

def delete_message(request, msg_id):
    Message.objects.get(id=msg_id).delete()
    return redirect('/wall')




