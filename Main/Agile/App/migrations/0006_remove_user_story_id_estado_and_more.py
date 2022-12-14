# Generated by Django 4.1 on 2022-12-04 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_estado_sprint_usuario_groups_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_story',
            name='id_estado',
        ),
        migrations.RemoveField(
            model_name='user_story',
            name='id_sprint',
        ),
        migrations.RemoveField(
            model_name='user_story',
            name='id_usuario',
        ),
        migrations.RemoveField(
            model_name='user_story',
            name='prioridad',
        ),
        migrations.AddField(
            model_name='backlog',
            name='id_estado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='App.estado_us'),
        ),
        migrations.AddField(
            model_name='backlog',
            name='id_usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='backlog',
            name='prioridad',
            field=models.IntegerField(default=0, verbose_name='Prioridad'),
        ),
    ]
