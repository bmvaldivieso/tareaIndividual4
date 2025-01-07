# Generated by Django 5.1.4 on 2025-01-02 18:54

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_cliente_altura_cliente_edad_cliente_peso'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluacionFisica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('porcentaje_grasa', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('resistencia_fisica', models.CharField(max_length=100)),
                ('fecha_registro', models.DateField(db_index=True)),
                ('notas_adicionales', models.TextField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_ultima_actualizacion', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'evaluacionfisica',
            },
        ),
    ]