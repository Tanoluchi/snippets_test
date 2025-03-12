# Respositorio django snippets

## Descripción

Aplicación en la cual usuarios registrados pueden crear Snippets de código en diferentes
lenguajes de programación.

## Requerimientos
    - Python 3.11
    - Django 5.1.2
    - SQLite
    - Pygments 

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/Tanoluchi/snippets_test.git
    ```

2. Crea un entorno virtual con Python >= 3.11

3. Instala los requerimientos:
    ```bash
    pip install -r requirements.txt
    ```

4. Ejecuta las migraciones para la base de datos
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Crea un usuario administrador y gestiona la creacion de usuarios
    ```bash
    python manage.py createsuperuser
    ```

6. Modifica el nombre del archivo de las variables de entorno a .env, luego configura los valores de las variables

7. Corre el proyecto y en paralelo también Celery para la ejecución de las tareas
    ```bash
    python manage.py runserver
    celery -A django_snippets worker -l info
    ```
