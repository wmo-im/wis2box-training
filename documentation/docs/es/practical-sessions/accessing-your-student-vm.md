---
title: Accediendo a tu VM de estudiante
---

# Accediendo a tu VM de estudiante

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, serás capaz de:

    - acceder a tu VM de estudiante mediante SSH y WinSCP
    - verificar que el software necesario para los ejercicios prácticos está instalado
    - verificar que tienes acceso a los materiales de los ejercicios para este entrenamiento en tu VM de estudiante local

## Introducción

Como parte de los talleres de capacitación de WIS2 realizados localmente, puedes acceder a tu VM de estudiante personal en la red de entrenamiento local llamada "WIS2-training".

Tu VM de estudiante tiene el siguiente software preinstalado:

- Ubuntu 22.04 LTS [ubuntu-22.04.5-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.5-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- Editores de texto: vim, nano

!!! note

    Si deseas realizar este entrenamiento fuera de una sesión de capacitación local, puedes proporcionar tu propia instancia utilizando cualquier proveedor de nube, por ejemplo:

    - GCP (Google Cloud Platform) VM instance `e2-medium`
    - AWS (Amazon Web Services) ec2-instance `t3a.medium`
    - Azure (Microsoft) Azure Virtual Machine `standard_b2s`

    Selecciona Ubuntu Server 22.0.4 LTS como sistema operativo.
    
    Después de crear tu VM, asegúrate de haber instalado python, docker y docker compose, como se describe en [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies).
    
    El archivo de lanzamiento de wis2box utilizado en este entrenamiento se puede descargar de la siguiente manera:

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.1.0/wis2box-setup-1.1.0.zip
    unzip wis2box-setup-1.1.0.zip
    ```
    
    Siempre puedes encontrar el archivo más reciente de 'wis2box-setup' en [https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases).

    El material de los ejercicios utilizado en este entrenamiento se puede descargar de la siguiente manera:

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    Los siguientes paquetes adicionales de Python son necesarios para ejecutar los materiales de los ejercicios:

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.2.2
    ```

    Si estás utilizando la VM de estudiante proporcionada durante las sesiones locales de capacitación de WIS2, el software necesario ya estará instalado.

## Conéctate a tu VM de estudiante en la red de entrenamiento local

Conecta tu PC a la red Wi-Fi local transmitida en el salón durante el entrenamiento de WIS2, según las instrucciones proporcionadas por el instructor.

Utiliza un cliente SSH para conectarte a tu VM de estudiante utilizando lo siguiente:

- **Host: (proporcionado durante el entrenamiento presencial)**
- **Port: 22**
- **Username: (proporcionado durante el entrenamiento presencial)**
- **Password: (proporcionado durante el entrenamiento presencial)**

!!! tip
    Contacta a un instructor si no estás seguro del nombre del host/usuario o si tienes problemas para conectarte.

Una vez conectado, por favor cambia tu contraseña para asegurarte de que otros no puedan acceder a tu VM:

```bash
limper@student-vm:~$ passwd
Changing password for testuser.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## Verifica las versiones del software

Para poder ejecutar wis2box, la VM de estudiante debe tener Python, Docker y Docker Compose preinstalados. 

Verifica la versión de Python:
```bash
python3 --version
```
devuelve:
```console
Python 3.10.12
```

Verifica la versión de Docker:
```bash
docker --version
```
devuelve:
```console
Docker version 24.0.6, build ed223bc
```

Verifica la versión de Docker Compose:
```bash
docker compose version
```
devuelve:
```console
Docker Compose version v2.21.0
```

Para asegurarte de que tu usuario puede ejecutar comandos de Docker, tu usuario ha sido añadido al grupo `docker`. 

Para probar que tu usuario puede ejecutar el comando hello-world de Docker, ejecuta el siguiente comando:
```bash
docker run hello-world
```

Esto debería descargar la imagen hello-world y ejecutar un contenedor que imprime un mensaje. 

Verifica que veas lo siguiente en la salida:

```console
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

## Inspecciona los materiales de los ejercicios

Inspecciona el contenido de tu directorio home; estos son los materiales utilizados como parte del entrenamiento y las sesiones prácticas.

```bash
ls ~/
```
devuelve:
```console
exercise-materials  wis2box
```

Si tienes WinSCP instalado en tu PC local, puedes usarlo para conectarte a tu VM de estudiante e inspeccionar el contenido de tu directorio home, así como descargar o subir archivos entre tu VM y tu PC local. 

WinSCP no es necesario para el entrenamiento, pero puede ser útil si deseas editar archivos en tu VM utilizando un editor de texto en tu PC local.

Aquí tienes cómo conectarte a tu VM de estudiante utilizando WinSCP:

Abre WinSCP y haz clic en "New Site". Puedes crear una nueva conexión SCP a tu VM de la siguiente manera:

<img alt="winscp-student-vm-scp.png" src="/../assets/img/winscp-student-vm-scp.png" width="400">

Haz clic en 'Save' y luego en 'Login' para conectarte a tu VM.

Y deberías poder ver el siguiente contenido:

<img alt="winscp-student-vm-exercise-materials.png" src="/../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## Conclusión

!!! success "¡Felicitaciones!"
    En esta sesión práctica, aprendiste a:

    - acceder a tu VM de estudiante mediante SSH y WinSCP
    - verificar que el software necesario para los ejercicios prácticos está instalado
    - verificar que tienes acceso a los materiales de los ejercicios para este entrenamiento en tu VM de estudiante local