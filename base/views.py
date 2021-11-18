from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *
import time

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="base/register.html", context={"register_form":form})
    

def LoginView(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password= password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is not correct.')

    context = {}
    return render(request, 'base\login.html', context)

def LogoutView(request):
    logout(request)
    return redirect('home')

def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)

def home(request):
    q = ''
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    roomMessages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        new_message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'roomMessages': roomMessages, 'participants': participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
            
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    # RESTRICT OTHER USERS TO UPDATE ROOM
    if request.user != room.host:
        return HttpResponse("<p>YOU ARE NOT ALLOWED TO EDIT ELSE'S ROOM!</p>")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    to_del = 'room'
    room = Room.objects.get(id=pk)

    # RESTRICT OTHER USERS TO DELETE ROOM
    if request.user != room.host:
        return HttpResponse("<p>YOU ARE NOT ALLOWED TO DELETE SOMEONE ELSE'S ROOM!</p>")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deletemsg(request, pk):
    to_del = 'msg'
    roomMessage = Message.objects.get(id=pk)
    # RESTRICT OTHER USERS TO DELETE MSG
    if request.user != roomMessage.user:
        return HttpResponse("<p>YOU ARE NOT ALLOWED TO DELETE SOMEONE ELSE'S MSG!</p>")

    if request.method == 'POST':
        roomMessage.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': roomMessage})