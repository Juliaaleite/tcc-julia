# Generated by Django 5.1.1 on 2024-11-26 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manutencao', '0002_alter_manutencao_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='manutencao',
            name='statusmanu',
            field=models.CharField(choices=[('A fazer', 'A fazer'), ('Concluído', 'Concluído')], default='A fazer', max_length=10),
        ),
    ]
