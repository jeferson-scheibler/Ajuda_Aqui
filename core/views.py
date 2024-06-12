from django.shortcuts import render

def register(request):
    return render(request, 'templates/register.html')

def create_task(request):
    return render(request, 'core/create_task.html')

def task_list(request):
    return render(request, 'core/task_list.html')