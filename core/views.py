from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, TaskForm
from .models import Task
from django.views.decorators.http import require_POST

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

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Associar a tarefa ao usuário logado
            task.save()
            messages.success(request, 'Tarefa criada com sucesso!')
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'create_task.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = TaskForm(instance=task)
    
    context = {
        'form': form,
        'task': task,
    }
    return render(request, 'edit_task_form.html', context)

@login_required
@require_POST
def update_task(request):
    task_id = request.POST.get('task_id')
    
    if not task_id:
        return JsonResponse({'error': 'ID da tarefa não fornecido'}, status=400)
    
    task = get_object_or_404(Task, id=task_id, user=request.user)
    form = TaskForm(request.POST, instance=task)
    
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    else:
        errors = form.errors.as_json()
        return JsonResponse({'error': errors}, status=400)
    
@login_required
def fetch_task_data(request):
    task_id = request.GET.get('task_id')
    task = get_object_or_404(Task, id=task_id, user=request.user)

    data = {
        'task_name': task.task_name,
        'task_description': task.task_description,
        'priority': task.priority,
        # Adicione outros campos conforme necessário
    }

    return JsonResponse(data)
