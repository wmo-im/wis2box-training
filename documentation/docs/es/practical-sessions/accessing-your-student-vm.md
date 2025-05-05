---
title: Accediendo a su VM de estudiante
---

# Accediendo a su VM de estudiante

!!! abstract "Objetivos de aprendizaje"

    Al final de esta sesión práctica, usted podrá:

    - acceder a su VM de estudiante mediante SSH y WinSCP
    - verificar que el software requerido para los ejercicios prácticos está instalado
    - verificar que tiene acceso a los materiales de ejercicios para esta capacitación en su VM local de estudiante

## Introducción

Como parte de las sesiones de capacitación de wis2box ejecutadas localmente, puede acceder a su VM personal de estudiante en la red local de capacitación denominada "WIS2-training".

Su VM de estudiante tiene el siguiente software preinstalado:

- Ubuntu 22.0.4.3 LTS [ubuntu-22.04.3-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.3-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- Editores de texto: vim, nano

!!! note

    Si desea ejecutar esta capacitación fuera de una sesión local de entrenamiento, puede proporcionar su propia instancia utilizando cualquier proveedor de nube, por ejemplo:

    - GCP (Google Cloud Platform) VM instance `e2-medium`
    - AWS (Amazon Web Services) ec2-instance `t3a.medium`
    - Azure (Microsoft) Azure Virtual Machine `standard_b2s`

    Seleccione Ubuntu Server 22.0.4 LTS como sistema operativo.
    
    Después de crear su VM, asegúrese de tener instalado python, docker y docker compose, como se describe en [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies).
    
    El archivo de lanzamiento para wis2box utilizado en esta capacitación se puede descargar de la siguiente manera:

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.0.0/wis2box-setup.zip
    unzip wis2box-setup.zip
    ```
    
    Siempre puede encontrar el último archivo 'wis2box-setup' en [https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases).

    El material de ejercicios utilizado en esta capacitación se puede descargar de la siguiente manera:

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    Los siguientes paquetes adicionales de Python son necesarios para ejecutar los materiales de ejercicios:

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.2.2
    ```

    Si está utilizando la VM de estudiante proporcionada durante las sesiones locales de capacitación WIS2, el software requerido ya estará instalado.

## Conectarse a su VM de estudiante en la red local de capacitación

Conecte su PC a la red Wi-Fi local transmitida en la sala durante la capacitación WIS2 según las instrucciones proporcionadas por el instructor.

Use un cliente SSH para conectarse a su VM de estudiante utilizando lo siguiente:

- **Host: (proporcionado durante la capacitación presencial)**
- **Puerto: 22**
- **Nombre de usuario: (proporcionado durante la capacitación presencial)**
- **Contraseña: (proporcionada durante la capacitación presencial)**

!!! tip
    Contacte a un instructor si no está seguro sobre el nombre de host/usuario o tiene problemas para conectarse.

Una vez conectado, cambie su contraseña para asegurarse de que otros no puedan acceder a su VM:

```bash
limper@student-vm:~$ passwd
Changing password for testuser.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## Verificar versiones de software

Para poder ejecutar wis2box, la VM del estudiante debe tener Python, Docker y Docker Compose preinstalados.

Verificar versión de Python:
```bash
python3 --version
```
devuelve:
```console
Python 3.10.12
```

Verificar versión de docker:
```bash
docker --version
```
devuelve:
```console
Docker version 24.0.6, build ed223bc
```

Verificar versión de Docker Compose:
```bash
docker compose version
```
devuelve:
```console
Docker Compose version v2.21.0
```

Para asegurar que su usuario pueda ejecutar comandos Docker, su usuario ha sido agregado al grupo `docker`.

Para probar que su usuario puede ejecutar docker hello-world, ejecute el siguiente comando:
```bash
docker run hello-world
```

Esto debería descargar la imagen hello-world y ejecutar un contenedor que imprime un mensaje.

Verifique que ve lo siguiente en la salida:

```console
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

## Inspeccionar los materiales de ejercicios

Inspeccione el contenido de su directorio personal; estos son los materiales utilizados como parte de la capacitación y sesiones prácticas.

```bash
ls ~/
```
devuelve:
```console
exercise-materials  wis2box
```

Si tiene WinSCP instalado en su PC local, puede usarlo para conectarse a su VM de estudiante e inspeccionar el contenido de su directorio personal y descargar o subir archivos entre su VM y su PC local.

WinSCP no es necesario para la capacitación, pero puede ser útil si desea editar archivos en su VM usando un editor de texto en su PC local.

Así es como puede conectarse a su VM de estudiante usando WinSCP:

Abra WinSCP y haga clic en "New Site". Puede crear una nueva conexión SCP a su VM de la siguiente manera:

<img alt="winscp-student-vm-scp.png" src="../../assets/img/winscp-student-vm-scp.png" width="400">

Haga clic en 'Save' y luego en 'Login' para conectarse a su VM.

Y debería poder ver el siguiente contenido:

<img alt="winscp-student-vm-exercise-materials.png" src="../../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## Conclusión

!!! success "¡Felicitaciones!"
    En esta sesión práctica, aprendió a:

    - acceder a su VM de estudiante mediante SSH y WinSCP
    - verificar que el software requerido para los ejercicios prácticos está instalado
    - verificar que tiene acceso a los materiales de ejercicios para esta capacitación en su VM local de estudiante