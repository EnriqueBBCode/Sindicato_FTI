# Generated by Django 5.1 on 2025-03-25 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario_salario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='roll',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuarios', to='usuarios.roll'),
        ),
    ]
