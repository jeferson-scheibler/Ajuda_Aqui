from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, TaskForm
from .models import Task, Feedback
from .forms import FeedbackForm
from django.template.loader import render_to_string
from django.db.models import Q

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback enviado com sucesso!')
            return redirect('index')
    else:
        form = FeedbackForm()
    return render(request, 'core/feedback.html', {'form': form})

def index(request):
    if request.user.is_authenticated:
        # Filtrar as tarefas excluindo as do usuário autenticado
        tasks = Task.objects.exclude(Q(user=request.user) | Q(completed=True))
    else:
        # Se não houver usuário autenticado, exibir todas as tarefas
        tasks = Task.objects.all()
    return render(request, 'core/index.html', {'tasks': tasks})

def about(request):
    return render(request, 'core/about.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, 'Registro realizado com sucesso!', extra_tags='success')
            return redirect('task_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}', extra_tags='error')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        remember_me = request.POST.get('remember_me')  # Captura o valor do checkbox "remember me"
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            response = redirect('task_list')
            response.set_cookie('username', user.username)
            # Evitar salvar a senha em cookies - Não é seguro
            # response.set_cookie('password', request.POST['password'])  # REMOVIDO
            
            if remember_me:
               request.session.set_expiry(1209600)  # 2 semanas
            else:
               #request.session.set_expiry(settings.SESSION_COOKIE_AGE)
               request.session.set_expiry(0)  # Expira ao fechar o navegador
            
            return response
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Tarefa criada com sucesso!', extra_tags='success')
            return redirect('task_list')
        else:
            messages.error(request, 'Erro ao criar a tarefa. Por favor, corrija os erros abaixo.', extra_tags='error')
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
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form})

@login_required
def update_task(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        task_id = request.POST.get('task_id')
        if task_id:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            form = TaskForm(request.POST, request.FILES, instance=task)
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
