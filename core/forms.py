# ajuda_aqui/core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Task

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
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('task_name', 'task_description', 'priority')

    def clean_priority(self):
        priority = self.cleaned_data['priority']
        if not priority:
            raise forms.ValidationError("Este campo é obrigatório.")
        return priority