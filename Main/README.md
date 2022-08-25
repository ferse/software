# software

## Instalacion del entorno virtual

py -3 -m venv .venv  

## Activar el entorno virtual

.\.venv\Scripts\activate

## Instalar librerias

pip install -r .\requirements.txt

## Iniciar el proyecto en modo DEV

cd .\Agile
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

## Crear archivo .env

## Agregar en .env el secret key

export SECRET_KEY = django-insecure-vjml*_vqs@(rw8fa(tndfw=__q-tci=&9=-)f8lg257rlse_hi