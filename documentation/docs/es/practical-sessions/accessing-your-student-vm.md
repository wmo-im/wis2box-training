---
title: Acceso a tu VM de estudiante
---

# Acceso a tu VM de estudiante

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, podrás:

    - acceder a tu VM de estudiante mediante SSH y WinSCP
    - verificar que el software requerido para los ejercicios prácticos esté instalado
    - verificar que tienes acceso a los materiales de los ejercicios para esta capacitación en tu VM de estudiante local

## Introducción

Como parte de las sesiones de capacitación de wis2box que se realizan localmente, puedes acceder a tu VM de estudiante personal en la red local de entrenamiento denominada "WIS2-training".

Tu VM de estudiante tiene el siguiente software preinstalado:

- Ubuntu 22.0.4.3 LTS [ubuntu-22.04.3-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.3-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- Editores de texto: vim, nano

!!! note

    Si deseas realizar esta capacitación fuera de una sesión de entrenamiento local, puedes proporcionar tu propia instancia utilizando cualquier proveedor de nube, por ejemplo:

    - Instancia VM de GCP (Google Cloud Platform) `e2-medium`
    - Instancia ec2 de AWS (Amazon Web Services) `t3a.medium`
    - Máquina Virtual Azure de Azure (Microsoft) `standard_b2s`

    Selecciona Ubuntu Server 22.0.4 LTS como sistema operativo.
    
    Después de crear tu VM asegúrate de haber instalado python, docker y docker compose, como se describe en [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies).
    
    El archivo de lanzamiento para wis2box utilizado en esta capacitación se puede descargar de la siguiente manera:

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.0.0/wis2box-setup.zip
    unzip wis2box-setup.zip
    ```
    
    Siempre puedes encontrar el último archivo de configuración de 'wis2box-setup' en [https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases).

    Los materiales de ejercicio utilizados en esta capacitación se pueden descargar de la siguiente manera:

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    Los siguientes paquetes adicionales de Python son necesarios para ejecutar los materiales de los ejercicios:

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.2.2
    ```

    Si estás utilizando la VM de estudiante proporcionada durante las sesiones locales de entrenamiento de WIS2, el software requerido ya estará instalado.

## Conéctate a tu VM de estudiante en la red local de entrenamiento

Conecta tu PC a la red Wi-Fi local transmitida en la sala durante el entrenamiento de WIS2 según las instrucciones proporcionadas por el entrenador.

Usa un cliente SSH para conectarte a tu VM de estudiante utilizando lo siguiente:

- **Host: (proporcionado durante el entrenamiento presencial)**
- **Puerto: 22**
- **Nombre de usuario: (proporcionado durante el entrenamiento presencial)**
- **Contraseña: (proporcionado durante el entrenamiento presencial)**

!!! tip
    Contacta a un entrenador si tienes dudas sobre el nombre de host/usuario o si tienes problemas para conectarte.

Una vez conectado, por favor cambia tu contraseña para asegurar que otros no puedan acceder a tu VM:

```bash
limper@student-vm:~$ passwd
Cambiando la contraseña para testuser.
Contraseña actual:
Nueva contraseña:
Repite la nueva contraseña:
passwd: contraseña actualizada correctamente
```

## Verifica las versiones del software

Para poder ejecutar wis2box, la VM de estudiante debería tener Python, Docker y Docker Compose preinstalados. 

Verifica la versión de Python:
```bash
python3 --version
```
devuelve:
```console
Python 3.10.12
```

Verifica la versión de docker:
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

Para asegurar que tu usuario pueda ejecutar comandos de Docker, tu usuario ha sido añadido al grupo `docker`. 

Para probar que tu usuario puede ejecutar docker hello-world, ejecuta el siguiente comando:
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

Inspecciona los contenidos de tu directorio home; estos son los materiales utilizados como parte de la capacitación y las sesiones prácticas.

```bash
ls ~/
```
devuelve:
```console
exercise-materials  wis2box
```

Si tienes WinSCP instalado en tu PC local, puedes usarlo para conectarte a tu VM de estudiante e inspeccionar los contenidos de tu directorio home y descargar o subir archivos entre tu VM y tu PC local. 

WinSCP no es necesario para la capacitación, pero puede ser útil si deseas editar archivos en tu VM usando un editor de texto en tu PC local.

Aquí te mostramos cómo puedes conectarte a tu VM de estudiante usando WinSCP:

Abre WinSCP y haz clic en "Nuevo sitio". Puedes crear una nueva conexión SCP a tu VM de la siguiente manera:

<img alt="winscp-student-vm-scp.png" src="/../assets/img/winscp-student-vm-scp.png" width="400">

Haz clic en 'Guardar' y luego en 'Iniciar sesión' para conectarte a tu VM.

Y deberías poder ver el siguiente contenido:

<img alt="winscp-student-vm-exercise-materials.png" src="/../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste cómo:

    - acceder a tu VM de estudiante mediante SSH y WinSCP
    - verificar que el software requerido para los ejercicios prácticos esté instalado
    - verificar que tienes acceso a los materiales de los ejercicios para esta capacitación en tu VM de estudiante local