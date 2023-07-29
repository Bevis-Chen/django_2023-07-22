from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login , logout, authenticate
from .models import Todo
from .forms import TodoForm
from datetime import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def completed_by_id(request, id):
    todo= Todo.objects.get(id= id, user= request.user)

    if todo.completed:
        todo.date_completed= datetime.now().strftime("%Y-%m-%d %H:%M%S")
        


@login_required
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

@login_required
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
                    temp_todo= form.save(commit= False)
                    if todo.completed:
                        temp_todo.date_completed= datetime.now().strftime(
                            "%Y-%m-%d %H:%M%S"
                        )
                    else:
                        temp_todo.date_completed= None
                    temp_todo.save()
                    # form.save()
                    message= "修改成功!"
        else:
            message= "請先登入...."
    except Exception as e:
        print(e)
        message= "無此代辦事項"

    return render(request, "./todo/view.html", {"todo": todo, "message":message, "user": user})

def get_todos(request, completed= False, reverse= False):
    user= request.user
    todos= None
    if user.is_authenticated:
        sort_command= "-created" if reverse else "created"
        todos= Todo.objects.filter(user= user, completed= completed).order_by(
            sort_command
        )
    return todos


@login_required
def completed(request):
    todos= get_todos(request, completed= True)
    return render(request, "./todo/completed.html", {"todos": todos})

def todo(request):
    user= request.user
    todos= None
    if user.is_authenticated:
        todos= Todo.objects.filter(user= user)
        print(todos)
    return render(request, "./todo/todo.html", {"todos": todos})