# Generated by Django 5.1.1 on 2024-11-26 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manutencao', '0003_manutencao_statusmanu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manutencao',
            name='statusmanu',
            field=models.CharField(default='A fazer', max_length=20),
        ),
    ]
