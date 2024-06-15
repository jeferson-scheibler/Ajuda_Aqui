from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, TaskForm
from .models import Task
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Ajuste para 'password1'
            user.save()
            login(request, user)
            messages.success(request, 'Registro realizado com sucesso!')
            return redirect('task_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')  # Mensagens de erro de validação
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Associar a tarefa ao usuário logado
            task.save()
            print(f"Tarefa criada com sucesso: {task}")  # Debug para verificar se a tarefa foi criada
            return redirect('task_list')  # Redirecionar para a lista de tarefas após criar a tarefa
        else:
            print(f"Erros no formulário: {form.errors}")  # Debug para verificar erros no formulário
    else:
        form = TaskForm()
    
    return render(request, 'create_task.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    print(tasks)  # Debugging: imprime as tarefas no console do servidor
    return render(request, 'task_list.html', {'tasks': tasks})
