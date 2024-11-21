from django import forms  # Importa o módulo de formulários do Django
from .models import Docente  # Importa os modelos Administrador e Docente
from django.contrib.auth.models import User  # Importa o modelo User para autenticação
from django.contrib.auth.forms import UserCreationForm  # Importa o formulário de criação de usuário do Django

# Formulário para cadastro de Administradores
class AdminRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Campo de e-mail obrigatório para o administrador

    class Meta:
        model = User  # Utiliza o modelo User para autenticação do administrador
        fields = ('username', 'email', 'password1', 'password2')  # Campos que serão exibidos no formulário

# Formulário para cadastro de Docentes
class DocenteForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Docente  # Especifica que o modelo para este formulário é o Docente
        fields = '__all__'  # Inclui todos os campos do modelo Docente no formulário
