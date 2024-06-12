from django.shortcuts import render

def register(request):
    return render(request, 'register.html')

def create_task(request):
    return render(request, 'create_task.html')

def task_list(request):
    return render(request, 'task_list.html') 
