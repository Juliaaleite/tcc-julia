# Generated by Django 5.1.1 on 2024-11-26 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manutencao', '0004_alter_manutencao_statusmanu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manutencao',
            name='statusmanu',
        ),
    ]
