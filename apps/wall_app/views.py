from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from apps.wall_app.models import User, UserManager, Message, List
from django.contrib import messages
import re, bcrypt


def index(request):
    return render(request, 'wall_temps/index.html')

def create(request):
    errors = User.objects.basic_validator(request.POST)
    if errors:
            print(errors)
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    else:
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['confirmpassword'].encode(), bcrypt.gensalt())
        )
        print("successfully created users")
        request.session['first_name']=request.POST['first_name']
        request.session['last_name']=request.POST['last_name']
        request.session['email']=request.POST['email']
        return redirect('/confirm')

def confirm(request):
    if 'email' not in request.session:
        return redirect('/')
    context = {
        "users" : User.objects.all(),
    }
    return render(request, "wall_temps/confirm.html", context)

def login(request):
    if User.objects.filter(email=request.POST['email']):
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print('email and password matches, successful login')
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['user_id'] = user.id
            request.session['email'] = user.email
            return redirect('/success')
        else:
            print("failed password")
            return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "items" : Message.objects.order_by("created_at")[:5],
        "users" : User.objects.all(),
    }
    print(request.session['user_id'])
    return render(request, "wall_temps/success.html", context)

def logout(request):
    request.session.clear()    
    return redirect('/')

def create_msg(request):
    Message.objects.create(name=request.POST["name"], user_id=request.session['user_id'])
    return redirect('/success')

def del_msg(request, id):
    d = Message.objects.get(id=id)
    if int(request.session['user_id']) == d.user_id:
        d.delete()
        return redirect('/success')
    else:
        print("You did not post this")
        return redirect('/success')

def show_others(request, id):
    return render(request, "wall_temps/show_item.html")
