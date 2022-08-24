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