from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.db.models import Manager
from django.db import models

class AdministradorManager(Manager):
    def create_user(self, email, password=None, **extra_fields):
        """Cria e retorna um usuário com um email e senha"""
        if not email:
            raise ValueError('O email deve ser definido')
        email = self.normalize_email(email)
        user = self.model(emailadm=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Cria e retorna um superusuário com um email e senha"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, emailadm):
        """Método necessário para autenticação"""
        return self.get(emailadm=emailadm)


class Docente(models.Model):
    nomedoc = models.CharField(max_length=150)
    emaildoc = models.EmailField(max_length=150)
    senhadoc = models.CharField(max_length=128)
    areaexecu = models.CharField(max_length=150)
    numidentdoc = models.IntegerField(primary_key=True)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'docente'

    # Métodos para integração com o sistema de autenticação do Django
    @property
    def is_authenticated(self):
        """Para ser compatível com o sistema de autenticação do Django"""
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_staff(self):
        return False

    @property
    def is_superuser(self):
        return False

class Maquina(models.Model):
    nomemaq = models.CharField(max_length=150)
    catmaq = models.CharField(max_length=150)
    codidentmaq = models.IntegerField(primary_key=True)
    manual_file = models.FileField(upload_to='media/manuais/', default='manuais/manual_default.pdf')
    image_file = models.FileField(upload_to='media/images/', default='images/image_default.png')
    class Meta:
        db_table = 'maquina'

from django.db import models

# Supondo que o modelo Maquina já esteja definido em algum lugar do seu projeto
from django.db import models

# Classe Manutencao
class Manutencao(models.Model):
    codidentmaq = models.ForeignKey(Maquina, on_delete=models.CASCADE)  # Relacionamento com Maquina
    descmanu = models.CharField(max_length=150)  # Descrição da manutenção
    codmanu = models.IntegerField(primary_key=True)  # Código único da manutenção
    tipomanu = models.CharField(max_length=150)  # Tipo de manutenção
    datamanu = models.DateField()  # Data da manutenção

    class Meta:
        db_table = 'manutencao'  # Nome da tabela no banco de dados
        verbose_name = 'Manutenção'  # Nome singular para exibição
        verbose_name_plural = 'Manutenções'  # Nome plural para exibição

    def __str__(self):
        return f'{self.descmanu} ({self.codmanu})'


# Classe Calendario (corrigida a indentação)
class Calendario(models.Model):
    id = models.BigAutoField(primary_key=True)
    codmanu = models.ForeignKey('Manutencao', on_delete=models.CASCADE)
    datamanu = models.DateTimeField()
    responmanu = models.CharField(max_length=255)
    tipomanu = models.CharField(max_length=100)

    class Meta:
        db_table = 'calendario'  # Caso você queira manter o nome da tabela especificado

    def __str__(self):
        return f"{self.responmanu} - {self.datamanu}"



class StatusMaquina(models.Model):
    codidentmaq = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='status_codidentmaq')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'statusmaquina'

class ManualMaquinas(models.Model):
    codidentmaq = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='manuais')  # Chave estrangeira para Maquina
    manmaq = models.CharField(max_length=255)  # Descrição ou outro campo relacionado ao manual
    codmanual = models.CharField(max_length=255)  # Código único do manual

    class Meta:
        db_table = 'ManualMaquinas'  # Nome da tabela no banco de dados
        unique_together = ('codidentmaq', 'codmanual')  # Garantir que a combinação de codidentmaq e codmanual seja única
 # Garante que o mesmo manual não seja associado à mesma máquina mais de uma vez
class Relatorios(models.Model):
    codmanu = models.ForeignKey(Manutencao, on_delete=models.CASCADE, related_name='relatorios_codmanu')
    datamanu = models.ForeignKey(Manutencao, on_delete=models.CASCADE, related_name='relatorios_datamanu')
    nomemaq = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='relatorios_nomemaq')
    imagem = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='relatorios_imagem')

    class Meta:
        db_table = 'relatorios'

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_admin=False, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, is_admin=is_admin, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='manutencao_user_groups',  # Evitar conflitos
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='manutencao_user_permissions',  # Evitar conflitos
        blank=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']
    objects = UserManager()
    def __str__(self):
        return self.email