# ajuda_aqui/core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Task, Feedback
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
        fields = ('task_name', 'task_description', 'priority', 'address', 'category', 'problem_photo', 'solution_photo','completed')
        labels = {
            'task_name': _('Nome da Tarefa'),
            'task_description': _('Descrição da Tarefa'),
            'priority': _('Prioridade'),
            'address': _('Endereço'),
            'category': _('Categoria'),
            'problem_photo': _('Foto do Problema'),
            'solution_photo': _('Foto da Solução'),
            'completed': _('Tarefa Concluída'),
        }
        widgets = {
            'task_name': forms.TextInput(attrs={'id': 'id_task_name', 'class': 'block w-full px-4 py-3 mt-2 text-gray-800 bg-white bg-opacity-90 border-2 rounded-lg border-gray-300 focus:border-yellow-500 focus:ring-opacity-50 focus:outline-none focus:ring focus:ring-yellow-400', 'placeholder': 'Nome da Tarefa'}),
            'task_description': forms.Textarea(attrs={'id': 'id_task_description', 'class': 'block w-full px-4 py-3 mt-2 text-gray-800 bg-white bg-opacity-90 border-2 rounded-lg border-gray-300 focus:border-yellow-500 focus:ring-opacity-50 focus:outline-none focus:ring focus:ring-yellow-400', 'rows': 3, 'placeholder': 'Descrição da Tarefa'}),
            'priority': forms.Select(attrs={'id': 'id_priority', 'class': 'block w-full px-4 py-3 mt-2 text-gray-800 bg-white bg-opacity-90 border-2 rounded-lg border-gray-300 focus:border-yellow-500 focus:ring-opacity-50 focus:outline-none focus:ring focus:ring-yellow-400'}),
            'address': forms.TextInput(attrs={'id': 'id_address', 'class': 'block w-full px-4 py-3 mt-2 text-gray-800 bg-white bg-opacity-90 border-2 rounded-lg border-gray-300 focus:border-yellow-500 focus:ring-opacity-50 focus:outline-none focus:ring focus:ring-yellow-400', 'placeholder': 'Endereço'}),
            'category': forms.Select(attrs={'id': 'id_category', 'class': 'block w-full px-4 py-3 mt-2 text-gray-800 bg-white bg-opacity-90 border-2 rounded-lg border-gray-300 focus:border-yellow-500 focus:ring-opacity-50 focus:outline-none focus:ring focus:ring-yellow-400'}),
            'problem_photo': forms.ClearableFileInput(attrs={'id': 'id_problem_photo', 'class': 'flex w-full rounded-md border border-yellow-300 border-input bg-white text-sm text-gray-400 file:border-0 file:bg-yellow-400 file:text-white file:text-sm file:font-medium '}),
            'solution_photo': forms.ClearableFileInput(attrs={'id': 'id_solution_photo', 'class': 'flex w-full rounded-md border border-yellow-300 border-input bg-white text-sm text-gray-400 file:border-0 file:bg-yellow-400 file:text-white file:text-sm file:font-medium'}),
            'completed': forms.CheckboxInput(attrs={'id': 'id_completed', 'class': 'px-4 py-2 bg-blue-500 text-white rounded cursor-pointer select-none'}),

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

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['content']
        labels = {
            'content': _('Digite aqui:'),
        }
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'placeholder': 'Valorizamos seu feedback! Conte-nos como podemos melhorar.',
                    'class': 'w-full bg-gray-100 text-gray-600 h-28 placeholder-gray-600 placeholder-opacity-50 border border-gray-200 col-span-6 resize-none outline-none rounded-lg p-2 mt-2 duration-300 focus:border-yellow-300 focus:ring-2 focus:ring-yellow-300'
                }
            )
        }

