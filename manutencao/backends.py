from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from manutencao.models import Docente, Administrador  # Ajuste conforme o nome do app

class DocenteBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            docente = Docente.objects.get(emaildoc=email)
            if check_password(password, docente.senhadoc):
                return docente
        except Docente.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Docente.objects.get(pk=user_id)
        except Docente.DoesNotExist:
            return None

class AdministradorBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            administrador = Administrador.objects.get(emailadm=email)
            if check_password(password, administrador.password):
                return administrador
        except Administrador.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Administrador.objects.get(pk=user_id)
        except Administrador.DoesNotExist:
            return None
