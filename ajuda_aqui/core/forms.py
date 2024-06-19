# ajuda_aqui/core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Se estiver usando um modelo personalizado
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Substitua por CustomUser se estiver usando um modelo personalizado
        fields = ('username', 'email', 'password1', 'password2')

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar Senha")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("As senhas não coincidem.")

        return cleaned_data