# Generated by Django 4.1 on 2022-09-08 01:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado_Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100, verbose_name='descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Estado_Us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100, verbose_name='descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100, verbose_name='descripcion')),
                ('duracion', models.IntegerField(verbose_name='duracion')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha Inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha Fin')),
            ],
        ),
        migrations.CreateModel(
            name='User_Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='nombre')),
                ('descripcion', models.CharField(max_length=100, verbose_name='descripcion')),
                ('fecha_creacion', models.DateField()),
                ('prioridad', models.IntegerField(verbose_name='Prioridad')),
                ('id_estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.estado_us')),
                ('id_sprint', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.sprint')),
                ('id_usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='nombre')),
                ('descripcion', models.CharField(max_length=100, verbose_name='descripcion')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('id_estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.estado_proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Backlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.proyecto')),
                ('id_us', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.user_story')),
            ],
        ),
    ]
