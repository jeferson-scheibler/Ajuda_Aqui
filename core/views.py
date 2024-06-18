from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, TaskForm
from .models import Task
from django.template.loader import render_to_string
from django.shortcuts import redirect


def index(request):
    return render(request, 'core/index.html')

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

# views.py

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        remember_me = request.POST.get('remember_me')  # Captura o valor do checkbox "remember me"
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if remember_me:
                # Define a duração do cookie de sessão
                request.session.set_expiry(1209600)  # 2 semanas
            else:
                request.session.set_expiry(0)  # Expira ao fechar o navegador
            
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
        print("Form fields:", form.fields)
        print("Task data:", task.task_name, task.task_description, task.priority)
    
    context = {
        'form': form,
        'task': task,
    }

@login_required
def update_task(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        task_id = request.POST.get('task_id')
        if task_id:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': form.errors}, status=400)
        else:
            return JsonResponse({'error': 'ID da tarefa não fornecido'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
@login_required
def fetch_task_data(request):
    task_id = request.GET.get('task_id')
    task = get_object_or_404(Task, id=task_id, user=request.user)
    form = TaskForm(instance=task)
    
    form_html = render_to_string('form_partial.html', {'form': form}, request=request)
    
    data = {
        'task_name': task.task_name,
        'task_description': task.task_description,
        'priority': task.priority,
        'form': form_html
    }

    return JsonResponse(data)

@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task_name = task.task_name  # Para pegar o nome da tarefa antes de excluir

        # Excluir a tarefa
        task.delete()

        # Redirecionar de volta para a página de lista de tarefas
        return redirect('task_list')

    # Se o método da requisição não for POST, retorna um erro
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def index(request):
    tasks = Task.objects.all()  # Busca todas as tarefas no banco de dados
    
    context = {
        'tasks': tasks
    }
    return render(request, 'index.html', context)