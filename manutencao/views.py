from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Manutencao, Docente, Maquina, StatusMaquina, ManualMaquinas, Relatorios, User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
import logging
from django import forms
from django.db.models import OuterRef, Subquery
from .models import Maquina, Manutencao
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models



# Crie um logger
logger = logging.getLogger(__name__)

def landingpage(request):
    return render(request, 'manutencao/entrar.html')

def manualwebadm(request):
    return render(request, 'manutencao/manualwebadm.html')

def manualwebdoc(request):
    return render(request, 'manutencao/manualwebdoc.html')

def base(request):
    return render(request, 'manutencao/base.html')

def base2(request):
    return render(request, 'manutencao/base2.html')



from django.urls import reverse
from .models import Maquina, StatusMaquina

def status_maquina(request):
    # Carregar todas as máquinas, com prefetch para os status
    maquinas = Maquina.objects.prefetch_related('status_codidentmaq').all()

    def toggle_machine_status(codidentmaq):
        # Encontre a instância da máquina usando o codidentmaq
        maquina = Maquina.objects.get(codidentmaq=codidentmaq)

        # Encontre o primeiro status da máquina
        status_maquina = StatusMaquina.objects.filter(codidentmaq=maquina).first()

        if status_maquina:
            # Altere o status da máquina
            status_maquina.status = not status_maquina.status
            status_maquina.save()
        else:
            # Se não houver status, cria um novo com a instância da máquina
            status_maquina = StatusMaquina.objects.create(codidentmaq=maquina, status=True)

        # Retorna o novo status da máquina
        return status_maquina.status

    if request.method == 'POST':
        codidentmaq = request.POST.get('codidentmaq')  # Corrigido para 'codidentmaq'
        if codidentmaq:
            # Tenta alternar o status da máquina
            toggle_machine_status(int(codidentmaq))
            return redirect(reverse('status_maquina'))
            # Redireciona de volta para a página de status das máquinas

    return render(request, 'manutencao/status_maquina.html', {'maquinas': maquinas})


@login_required
def calendariodoc(request):
    # Obtenha os eventos para exibir no calendário
    eventos_calendario = Manutencao.objects.all().order_by('datamanu')

    # Contexto para o template
    context = {
        'eventos': eventos_calendario,
        'current_year': datetime.now().year,
        'current_month': datetime.now().month
    }

    # Renderiza o template do calendário
    return render(request, 'manutencao/calendariodoc.html', context)


def calendarioadm(request):
    eventos_calendario = Manutencao.objects.all().order_by('datamanu')

    context = {
        'eventos': eventos_calendario,
        'current_year': datetime.now().year,
        'current_month': datetime.now().month

    }

    return render(request, 'manutencao/calendarioadm.html', context)

from django.http import JsonResponse

def obter_eventos(request):
    eventos_calendario = Manutencao.objects.all()
    eventos = {}

    for evento in eventos_calendario:
        data = evento.datamanu.strftime('%Y-%m-%d')  # Formatar a data
        if data not in eventos:
            eventos[data] = []
        eventos[data].append({
            'descricao': evento.descmanu,
            'tipomanutencao': evento.tipomanu,
            'responmanu': evento.responmanu,
        })

    return JsonResponse(eventos)

def manual_maquinas(request):
    maquinas = Maquina.objects.all()  # Obtém todas as máquinas cadastradas
    return render(request, 'manutencao/manual_maquina.html', {'maquinas': maquinas})

def manual_maquinasadm(request):
    maquinas = Maquina.objects.all()  # Obtém todas as máquinas cadastradas
    return render(request, 'manutencao/manual_maquinaadm.html', {'maquinas': maquinas})

from .models import User

# Configuração do logger
logger = logging.getLogger(__name__)


def cadastro(request):
    logger.info("Acessando a função de cadastro.")  # Log de entrada na função

    if request.method == 'POST':
        logger.info("Recebendo dados do formulário de cadastro.")  # Log para POST

        # Coletar os dados do formulário
        nome = request.POST.get('nome_doc')
        email = request.POST.get('email_doc')
        senha = request.POST.get('senha_doc')
        is_admin = request.POST.get('is_admin') == 'True'

        logger.debug(f"Dados recebidos - Nome: {nome}, Email: {email}, Is Admin: {is_admin}")

        # Verificar duplicação de e-mail
        if User.objects.filter(email=email).exists():
            logger.warning(f"Tentativa de cadastro com e-mail duplicado: {email}")
            messages.error(request, "O email já está em uso. Tente outro.")
            return render(request, 'manutencao/cadastro.html')

        try:
            # Criar o usuário
            user = User.objects.create_user(
                email=email,
                password=senha,
                nome=nome,
                is_admin=is_admin
            )
            logger.info(f"Usuário criado com sucesso: {email}")
        except Exception as e:
            logger.error(f"Erro ao criar o usuário: {e}")
            messages.error(request, "Erro ao criar o usuário. Por favor, tente novamente.")
            return render(request, 'manutencao/cadastro.html')

        # Redirecionar para a página de login
        messages.success(request, "Cadastro realizado com sucesso! Faça login para continuar.")
        logger.info("Cadastro realizado com sucesso. Redirecionando para a tela de login.")
        return redirect('entrarDOC')

    logger.info("Renderizando página de cadastro.")
    return render(request, 'manutencao/cadastro.html')

from django.http import HttpResponse
from .models import Maquina, ManualMaquinas

def cadastrar_maquina(request):
    if request.method == 'POST':
        nomemaq = request.POST.get('nomemaq')
        catmaq = request.POST.get('catmaq')
        codidentmaq = request.POST.get('codidentmaq')
        manual = request.FILES.get('manual')
        image = request.FILES.get('image')

        # Adicione logs para verificar os dados recebidos
        print(f"Recebido - Nome: {nomemaq}, Categoria: {catmaq}, Código: {codidentmaq}, Manual: {manual}, Image: {image}")

        try:
            # Primeiro, crie um registro em Maquina
            maquina = Maquina(
                nomemaq=nomemaq,
                catmaq=catmaq,
                codidentmaq=codidentmaq,
                manual_file=manual,
                image_file=image
            )
            maquina.save()  # Salva o registro de Maquina

            # Agora, crie um registro em ManualMaquinas usando o ID da Maquina recém-criada
            manual_maquinas = ManualMaquinas(
                manmaq=manual.name,  # Nome do manual ou outro campo relevante
                codidentmaq=maquina,  # Referência à Maquina recém-criada
            )
            manual_maquinas.save()  # Salva o registro de ManualMaquinas

            print("Máquina e manual salvos com sucesso!")
            return redirect('calendarioadm')  # Redireciona para uma página de sucesso
        except Exception as e:
            print(f"Erro ao salvar a máquina: {e}")
            return HttpResponse("Erro ao salvar a máquina.")

    return render(request, 'manutencao/cadastro_maquina.html')

from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('emaildoc')
        senha = request.POST.get('senhadoc')

        user = authenticate(request, email=email, password=senha)

        if user:
            login(request, user)
            return redirect('calendarioadm' if user.is_admin else 'calendariodoc')
        else:
            messages.error(request, "Credenciais inválidas. Tente novamente.")

    return render(request, 'manutencao/entrar.html')

@login_required
def admin_home(request):
    return render(request, 'manutencao/calendarioadm.html')

@login_required
def docente_home(request):
    return render(request, 'manutencao/calendariodoc.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Docente, Maquina, Manutencao

@login_required
def cadastro_manutencao(request):
    if request.method == 'POST':
        # Recebe os dados do formulário
        codidentmaq = request.POST.get('codidentmaq')
        tipomanu = request.POST.get('tipomanu')  # Tipo de manutenção
        datamanu = request.POST.get('datamanu')  # Data da manutenção
        descmanu = request.POST.get('descmanu')  # Descrição da manutenção

        # Verifica se a máquina com o código de identificação existe
        maquina = Maquina.objects.filter(codidentmaq=codidentmaq).first()
        if not maquina:
            error_message = "ID da máquina não encontrado."
            return render(request, 'manutencao/cadastro_manutencao.html', {'error_message': error_message})

        # Tenta criar a nova manutenção
        try:
            nova_manutencao = Manutencao(
                codidentmaq=maquina,
                descmanu=descmanu,
                tipomanu=int(tipomanu),  # Certifique-se de que isso é um inteiro
                datamanu=datamanu,
            )
            nova_manutencao.save()  # Salva o objeto
            return redirect('calendariodoc')  # Redireciona após o sucesso
        except Exception as e:
            error_message = f"Erro ao salvar a manutenção: {str(e)}"
            return render(request, 'manutencao/cadastro_manutencao.html', {'error_message': error_message})

    # Se o método não for POST, apenas renderiza a página de cadastro
    return render(request, 'manutencao/cadastro_manutencao.html')


from django.shortcuts import render, redirect
from .models import Manutencao
from django.contrib.auth.decorators import login_required


@login_required
def manutencao_list(request):
    # Recupera todas as manutenções
    manutencao_lista = Manutencao.objects.all()

    # Passa as manutenções para o template
    return render(request, 'manutencao/manutencao_list.html', {'manutencao_lista': manutencao_lista})


def relatorios(request):
    # Subquery para pegar a última manutenção de cada máquina
    ultima_manutencao = Manutencao.objects.filter(
        codidentmaq=OuterRef('pk')
    ).order_by('-datamanu')  # Ordena pela data da manutenção, da mais recente para a mais antiga

    # Consultar todas as máquinas e anexar a última manutenção
    maquinas = Maquina.objects.annotate(
        ultima_manutencao=Subquery(ultima_manutencao.values('descmanu')[:1]),  # Obtem a descrição da última manutenção
        data_ultima_manutencao=Subquery(ultima_manutencao.values('datamanu')[:1])  # Obtem a data da última manutenção
    )

    return render(request, 'manutencao/pdfadm.html', {'maquinas': maquinas})

class DocenteManager(BaseUserManager):
    def create_user(self, emaildoc, senhadoc, **extra_fields):
        if not emaildoc:
            raise ValueError('O email deve ser preenchido.')
        user = self.model(emaildoc=emaildoc, **extra_fields)
        user.set_password(senhadoc)
        user.save(using=self._db)
        return user

    def create_superuser(self, emaildoc, senhadoc, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(emaildoc, senhadoc, **extra_fields)