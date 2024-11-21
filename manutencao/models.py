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
    manual_file = models.FileField(upload_to='media/manuais/', default='manuais/manual_default.pdf')  # Valor padrão
    image_file = models.FileField(upload_to='media/images/', default='images/image_default.png')

    class Meta:
        db_table = 'maquina'

class Manutencao(models.Model):
    codidentmaq = models.ForeignKey('Maquina', on_delete=models.CASCADE)
    numidentdoc = models.ForeignKey('Docente', on_delete=models.CASCADE)
    descmanu = models.CharField(max_length=150)
    codmanu = models.IntegerField(primary_key=True)
    tipomanu = models.IntegerField()
    datamanu = models.DateField()

    class Meta:
        db_table = 'manutencao'

class StatusMaquina(models.Model):
    codidentmaq = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='status_codidentmaq')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'statusmaquina'

class ManualMaquinas(models.Model):
    codidentmaq = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='manuais')
    manmaq = models.CharField(max_length=255)
    codmanual = models.CharField(max_length=255)  # Remova primary_key=True

    class Meta:
        db_table = 'ManualMaquinas'
        unique_together = ('codidentmaq', 'codmanual')  # Garante que o mesmo manual não seja associado à mesma máquina mais de uma vez
class Relatorios(models.Model):
    codmanu = models.ForeignKey(Manutencao, on_delete=models.CASCADE, related_name='relatorios_codmanu')
    datamanu = models.ForeignKey(Manutencao, on_delete=models.CASCADE, related_name='relatorios_datamanu')
    nomemaq = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='relatorios_nomemaq')
    imagem = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='relatorios_imagem')

    class Meta:
        db_table = 'relatorios'

class Calendario(models.Model):
    codmanu = models.ForeignKey(Manutencao, on_delete=models.CASCADE, related_name='calendarios_codmanu')
    datamanu = models.ForeignKey(Manutencao, on_delete=models.CASCADE, related_name='calendarios_datamanu')
    responmanu = models.ForeignKey(Manutencao, on_delete=models.CASCADE, related_name='calendarios_responmanu')
    tipomanu = models.ForeignKey(Manutencao, on_delete=models.CASCADE, related_name='calendarios_tipomanu')

    class Meta:
        db_table = 'Calendario'

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
