# Generated by Django 5.1 on 2025-03-25 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='salario',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
