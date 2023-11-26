# Backend simple en Flask (no terminado)

Bienvenido! En este proyecto estoy desarrollando una API simple en Flask. Aquí se están aplicando varias tecnologías y metodologías, pero en particular estoy aprendiendo a usar Flask y el entorno virtual venv de python, por lo que no esperes un proyecto perfecto.

## Descarga ⬇️

Si deseas obtener una copia local, descarga el archivo comprimido .zip desde el botón verde "code" o haz click [aquí](https://github.com/Ale6100/backend-simple-flask/archive/refs/heads/main.zip)

### Pre-requisitos 📋
Necesitas tener previamente descargado e instalado [Python](https://www.python.org/). En mi caso, estoy usando la version 3.12.0

### Instalación (en windows) 🔧
Crea un entorno virtual con el comando

```
py -3 -m venv .venv
```

Luego actívalo con el comando

```
.venv\Scripts\activate
```

A continuación, instala las dependencias con el comando

```
pip install -r requirements.txt
```

Es necesario crear variables de entorno mediante la elaboración de un archivo .env en el mismo nivel que la carpeta src. Este archivo debe completarse con los siguientes campos, los cuales deben modificarse con tus propias credenciales en lugar del valor "X":

```env
DB_HOST = X # Estos cuatro valores corresponden a tus credenciales de la base de datos
DB_USER = X
DB_PASSWORD = X
DB_DATABASE = X

URL_FRONTEND1 = x # URL del frontend que desees dar permisos de acceso, sin barra lateral final
```

## Despliegue 📦
Inicia el servidor web Flask en modo de depuración:

```
flask run --debug
```

Recuerda siempre tener activado el entorno virtual antes de empezar.
