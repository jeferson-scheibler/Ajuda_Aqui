from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


def register(request):
    return render(request, 'register.html')

def create_task(request):
    return render(request, 'create_task.html')

def task_list(request):
    return render(request, 'task_list.html') 
