from django.contrib import admin
from .models import Docente, Maquina, Manutencao, StatusMaquina, ManualMaquinas,  Relatorios, Calendario

admin.site.register(Docente)

admin.site.register(Maquina)

admin.site.register(Manutencao)

admin.site.register(StatusMaquina)

admin.site.register(ManualMaquinas)

admin.site.register(Relatorios)

admin.site.register(Calendario)
