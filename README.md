# Repositorio django snippets

## Descripción

Aplicación en la cual usuarios registrados pueden crear Snippets de código en diferentes
lenguajes de programación.

## Requerimientos
    - Python 3.11
    - Django 5.1.2
    - SQLite
    - Pygments 

## Instalación y configuración

### Manera manual

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

6. Cambiar nombre de archivo .env.example a .env, luego configura los valores de las variables
```bash
        # Configuracion Django
        SECRET_KEY="THEWINTERISCOMING"
        DEBUG=True

        # Configuracion de email para la task
        EMAIL_HOST="smtp.gmail.com"
        EMAIL_HOST_USER="yourmail@gmail.com"
        EMAIL_HOST_PASSWORD="your pasword"
        EMAIL_PORT=587
        EMAIL_USE_TLS=True

        # Configuracion redis
        REDIS_URL="redis://127.0.0.1:6379"

        # Configuracion celery para usarlo en tests
        CELERY_EAGER=False

        # Configuracion para utilizar base de datos local o de produccion
        IS_PRODUCTION=False

        # Configuracion base de datos (vacio si no es de produccion ya que utilizaremos sqlite en entorno de desarrollo)
        DATABASE_URL=""
```

7. Levanta tu servidor redis

8. Corre el proyecto y en paralelo también Celery para la ejecución de las tareas
    ```bash
    python manage.py runserver
    celery -A django_snippets worker -l info
    ```

### Usando Docker

1. Cambiar nombre de archivo .env.example a .env y luego modificar el archivo
     ```bash
        # Configuracion Django
        SECRET_KEY="THEWINTERISCOMING"
        DEBUG=True

        # Configuracion de email para la task
        EMAIL_HOST="smtp.gmail.com"
        EMAIL_HOST_USER="yourmail@gmail.com"
        EMAIL_HOST_PASSWORD="your pasword"
        EMAIL_PORT=587
        EMAIL_USE_TLS=True

        # Configuracion redis
        REDIS_URL="redis://snippets_test-redis:6379"

        # Configuracion celery para usarlo en tests
        CELERY_EAGER=False

        # Configuracion para utilizar base de datos local o de produccion
        IS_PRODUCTION=False

        # Configuracion base de datos (vacio si no es de produccion ya que utilizaremos sqlite en entorno de desarrollo)
        DATABASE_URL=""
    ```

2.Levantar el docker con el siguiente comando
```bash
    - make build
    - make up
```

3. Crear un superusuario con el comando
```bash
    - make exec
    - python manage.py createsuperuser
```

4. Correr celery con el comando
```bash
    - make celery
```

## Credenciales
- username: admin
- password: admin123

## URL Production
https://web-production-51c1f.up.railway.app/