from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import login , logout, authenticate
from .models import Todo

# Create your views here.


def todo(request):
    user= request.user
    if user.is_authenticated:
        todos= Todo.objects.filter(user= user)
        print(todos)


    return render(request, "./todo/todo.html", {"user":user})