# Generated by Django 4.1 on 2022-08-20 01:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Formulario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='nombre')),
                ('descripcion', models.CharField(max_length=100, verbose_name='descripcion')),
                ('id_formulario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.formulario')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='nombre')),
                ('descripcion', models.CharField(max_length=100, verbose_name='descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('alias', models.CharField(max_length=20, unique=True, verbose_name='alias')),
                ('email', models.EmailField(max_length=60, verbose_name='email')),
                ('nombre', models.CharField(max_length=20, verbose_name='nombre')),
                ('apellido', models.CharField(max_length=20, verbose_name='apellido')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Usuario_Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_desde', models.DateField()),
                ('fecha_hasta', models.DateField()),
                ('id_rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.rol')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rol_Permiso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_permiso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.permiso')),
                ('id_rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.rol')),
            ],
        ),
    ]
