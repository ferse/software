# Generated by Django 4.1 on 2022-08-25 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Formulario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fdescripcion', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'formulario',
            },
        ),
    ]