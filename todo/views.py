from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login , logout, authenticate
from .models import Todo
from .forms import TodoForm


# Create your views here.

def create(request):
    message= ""
    form = TodoForm()
    if request.method == "POST":
        print(request.POST)
        form= TodoForm(request.POST)
        if form.is_valid():
            todo= form.save(commit= False)
            todo.user= request.user
            todo.save()
            message= "建立todo成功!"


    return render(request, "./todo/create.html", {"form": form, "message": message})


def view(request, id):
    message= ""
    form, todo= None, None
    user= request.user
    try: 
        if user.is_authenticated:
            todo= Todo.objects.get(id= id, user= request.user)
            form= TodoForm(instance= todo)
            if request.method== "POST":
                form= TodoForm(request.POST, instance= todo)
                if form.is_valid():
                    form.save()
                    message= "修改成功!"
        else:
            message= "請先登入...."
    except Exception as e:
        print(e)
        message= "無此代辦事項"

    return render(request, "./todo/view.html", {"todo": todo, "message":message, "user": user})


def todo(request):
    user= request.user
    todos= None
    if user.is_authenticated:
        todos= Todo.objects.filter(user= user)
        print(todos)


    return render(request, "./todo/todo.html", {"todos": todos})