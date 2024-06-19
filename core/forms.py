# ajuda_aqui/core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Task
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Senha")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2
        
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('task_name', 'task_description', 'priority', 'address', 'completed', 'category', 'problem_photo', 'solution_photo')
        labels = {
            'task_name': _('Nome da Tarefa'),
            'task_description': _('Descrição da Tarefa'),
            'priority': _('Prioridade'),
            'address': _('Endereço'),
            'completed': _('Tarefa Concluída'),
            'category': _('Categoria'),
            'problem_photo': _('Foto do Problema'),
            'solution_photo': _('Foto da Solução'),
        }
        widgets = {
            'task_name': forms.TextInput(attrs={'id': 'id_task_name', 'class': 'form-control', 'placeholder': 'Nome da Tarefa'}),
            'task_description': forms.Textarea(attrs={'id': 'id_task_description', 'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição da Tarefa'}),
            'priority': forms.Select(attrs={'id': 'id_priority', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'id': 'id_address', 'class': 'form-control', 'placeholder': 'Endereço'}),
            'completed': forms.CheckboxInput(attrs={'id': 'id_completed', 'class': 'form-check-input'}),
            'category': forms.Select(attrs={'id': 'id_category', 'class': 'form-control'}),
            'problem_photo': forms.ClearableFileInput(attrs={'id': 'id_problem_photo', 'class': 'form-control-file'}),
            'solution_photo': forms.ClearableFileInput(attrs={'id': 'id_solution_photo', 'class': 'form-control-file'}),
        }

    def clean_priority(self):
        priority = self.cleaned_data['priority']
        if not priority:
            raise forms.ValidationError("Este campo é obrigatório.")
        return priority

    def clean_task_name(self):
        task_name = self.cleaned_data['task_name']
        if len(task_name) < 5:
            raise forms.ValidationError("O nome da tarefa deve ter pelo menos 5 caracteres.")
        return task_name