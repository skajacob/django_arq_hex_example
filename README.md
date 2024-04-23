# API django_assesment
En este proyecto se implementa una API REST con arquitectura hexagonal y desarrollo basado en unittest de compoortamieto.

## Clonar repositorio

```
git clone https://github.com/skajacob/django_arq_hex_example.git
```

## Bases de datos:
- **PostgreSQL** : Se utiliza para almacenar la información interna de la aplicación

`NOTA: De acuerdo a lo propuesto en la HU_SPRINT.md se genera un diagrama de entidad relación en un png`

## Desplegar proyecto

1. Crea tu ambiente virtual ejecuta el siguiente comando:

   ```ssh
   py -m venv venv;
   venv\Scripts\activate
   ```

2. Instala las dependencias del proyecto:

   ```ssh
    pip install -r requirements.txt
    ```

3. Crear una base de datos cheaf-db en postgres 
```
   createdb -U postgres -W -h 127.0.0.1 -p 5432 cheaf-db 
 ```
4. Situate en la carpeta del proyecto para crear tu archivo .env pon tus credenciales de la bases de datos y tu correo con la contraseña para el servicio de notificaciones
   ```ssh
    DEBUG=True
    SECRET_KEY='11111111111818181818181811111111'
    ALLOWED_HOSTS=*
    
    #redis
    REDIS_HOST=127.0.0.1
    REDIS_PORT=6379
    REDIS_DB_NAME = 0
    
    # Database
    DB_USER=
    DB_PASSWORD=
    DB_HOST=127.0.0.1
    DB_PORT=5432
    DB_NAME=cheaf-db
    DB_ENGINE=django.contrib.gis.db.backends.postgis

    # email service 
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER=
    EMAIL_HOST_PASSWORD=

    # GDAL and GEOS settings
    GDAL_LIBRARY_PATH =C:/OSGeo4W/bin/gdal307.dll
    GEOS_LIBRARY_PATH=C:/OSGeo4W/bin/geos_c.dll
    

    ```
    NOTA: SI NO TIENES LAS LIBREARIAS DE GEODJANGO ELIMINAR DEL SETTING.PY LA CONFIGURACION DE GEODJANGO Y SUSTITUIR POR VARIABLE DB_ENGINE = django.db.backends.postgresql_psycopg2
    ```
       
   ``` 
5. En la misma carpeta ejecuta las migraciones

   ```ssh
   python manage.py makemigrations;
   python manage.py migrate
   ```
6. Ahora instala los fixtures para el dummy data

   ```ssh
   python manage.py loaddata .\fixtures\data.json
   ```
   
6. Inicia el servidor

   ```ssh
    python manage.py runserver
    ```
7. En una terminal nueva nicia el redis-servidor(descargar Redis-x64-3.0.504.zip en 
 https://github.com/microsoftarchive/redis/releases y agregarla a las variables de entorno)

   ```redis-server 
    ```
8. En un terminal nueva inicia el cronjob

   ```celery -A apps.webApp worker --loglevel=info
    ```

## Desplegar proyecto con docker

1. construye la imagen

   ```ssh
   docker compose build
   ```
2. Crea el contenedor de la base

   ```ssh
    docker compose up -d db
    ```
3. Crea el contenedor de la api

   ```ssh
    docker compose up
    ```
4. Lista los contenedores para obtener los ids

   ```ssh
    docker ps
    ```
   
5. Ingresa al contenedor de la base para instalar postgis y poder hacer migraciones

   ```ssh
    docker exec -it <id_container> bash
    ```

6. Instala postgis

   ```ssh
    apt-get update
    apt-get install -y postgis
    ```

7. Crea la extension de postgres

    ```ssh
     psql -U postgres -c "CREATE EXTENSION postgis;"
     ```

8. Crea las migraciones en el contenedor de la api
    
    ```ssh
    docker exec -it <id_container> bash
    python manage.py makemigrations;
    python manage.py migrate
    ```

   
### Info del proyecto

Este proyecto fue desarrollado basado en una practica la cuál es generar contratos para el backend los cuales
pérmitan de manera sencilla la integración de los servicios y la comunicación entre los mismos.

Se generó un documento CONTRATO-HU-1-Products.md el cual contiene los contratos de los servicios que se implementaron en el proyecto.
El proyecto cuenta con dos usuarios cargados en los fixtures. Los usuarios tienen dos perfiles, super_administrator y administrator.


- **super_administrator** : Puede crear, editar y eliminar productos y crear alarmas
- **administrator** : Solo puede ver los productos

Las credenciales de cada uno son las siguientes:

- **super_administrator** :
  - email: dj-superadmin@cheaf.io 
  - password: admin123
- **administrator** :
  - email: dj-admin@cheaf.io 
  - password: admin123



La api está documentada en el url:

http://localhost:8000/api/swagger/

usa el servicio de token/ para obtener el token de autenticación y usa el token en el Authorize con la palabra Bearer antes del token.

`EJEMPLO: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY5ODQ4MDQwLCJpYXQiOjE2Njk4NDc3NDAsImp0aSI6IjQwYTQ0MGRkYTk1MjRjYTliYmRlNTUwODMzZjYwMGQwIiwidXNlcl9pZCI6MX0.11mvl3StKfxX0hwKVHXzgSdlI0TUN7kJEEVPeaeLdYg`

### Ejecutar pruebas

Para ejecutar las pruebas unitarias ejecuta el siguiente comando

```ssh
python manage.py test
```


## Pre-commit y commitzen configuration

Para configurar el pre-commit y commitzen ejecuta los siguientes comandos

1. Instalacion de choco para instalar makefile en windows - ejecutar como administrador

   ```ssh
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. Instalacion de makefile

   ```ssh
    choco install make
    ```
3. Comprobamos que exista make

    ```ssh
     make -v
     ```
4. Instalacion de pre-commit

    ```ssh
    pre-commit install
     ```

## Flujo de integracion y versionado

1. Se formatea el codigo con la funcion de nuestro makefile "format"

    ```ssh
    make format
     ```

2. Se agregan los archivos a staged y se genera el commitzen para generar el mensaje de commit

    ```ssh
    git add .; git cz commit
     ```
3. Se hace push
    
    ```ssh
    git push
    ```









