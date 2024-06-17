"""
URL configuration for ajuda_aqui project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views  # Importando views do diretório core

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_task/', views.create_task, name='create_task'),
    path('task-list/', views.task_list, name='task_list'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('update_task/', views.update_task, name='update_task'),
    path('fetch_task_data/', views.fetch_task_data, name='fetch_task_data'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
]

