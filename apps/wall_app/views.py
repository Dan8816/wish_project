from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from apps.wall_app.models import User, UserManager, Wish
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
            hire = request.POST['hire'],
            password = bcrypt.hashpw(request.POST['confirmpassword'].encode(), bcrypt.gensalt())
        )
        print(request.POST['hire'])
        print("successfully created users")
        request.session['user_id']=new_user.id
        request.session['first_name']=request.POST['first_name']
        request.session['last_name']=request.POST['last_name']
        request.session['email']=request.POST['email']
        return redirect('/success')

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
    UserList = {
        "wishlist" : Wish.objects.filter(wisher_id=request.session['user_id']).order_by("created_at"),
        "others" : Wish.objects.filter(wishes=request.session['user_id']).order_by("created_at"),
        "otherwishes" : Wish.objects.exclude(wisher_id=request.session['user_id']).order_by("created_at")
    }
    return render(request, "wall_temps/success.html", UserList)

def logout(request):
    request.session.clear()    
    return redirect('/')

def make_wish(request):
    return render(request, "wall_temps/make_wish.html")

def create_wish(request):
    Wish.objects.create(wisher_id=request.session['user_id'], item_name=request.POST["item_name"])
    return redirect('/success')

def del_wish(request, id):
    d = Wish.objects.get(id=id)
    if int(request.session['user_id']) == d.wisher_id:
        d.delete()
        return redirect('/success')
    else:
        print("You did not wish this")
        return redirect('/success')

def user_wishes(request, id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_wish = Wish.objects.get(id=id)
    this_wish.wishes.add(this_user)
    this_wish.save()
    return redirect('/success')

def item_wishes(request, item_name):
    context = {
        "wishes" : Wish.objects.filter(item_name=item_name),
    }
    print(context)
    return render(request, "wall_temps/this_item.html", context)

def remove_wishes(request, id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_wish = Wish.objects.get(id=id)
    this_wish.wishes.remove(this_user)
    this_wish.save()
    return redirect('/success')