# Generated by Django 5.1.4 on 2025-01-03 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_cliente_cedula'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrenador',
            name='cargo',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='cedula',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='direccion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='experiencia_laboral',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='idioma1',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='idioma2',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
