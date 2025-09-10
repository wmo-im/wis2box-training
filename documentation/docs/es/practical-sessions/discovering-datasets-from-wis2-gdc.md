---
title: Descubriendo conjuntos de datos del WIS2 Global Discovery Catalogue
---

# Descubriendo conjuntos de datos del WIS2 Global Discovery Catalogue

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, serás capaz de:

    - usar pywiscat para descubrir conjuntos de datos del Global Discovery Catalogue (GDC)

## Introducción

En esta sesión aprenderás a descubrir datos del WIS2 Global Discovery Catalogue (GDC) utilizando [pywiscat](https://github.com/wmo-im/pywiscat), una herramienta de línea de comandos para buscar y recuperar metadatos de un GDC de WIS2.

Actualmente, los siguientes GDC están disponibles:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration: <https://gdc.wis.cma.cn>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc>

Durante las sesiones de formación local, se configura un GDC local para permitir a los participantes consultar el GDC por los metadatos que publicaron desde sus instancias de wis2box. En este caso, los instructores proporcionarán la URL del GDC local.

## Preparación

!!! note
    Antes de comenzar, por favor inicia sesión en tu máquina virtual de estudiante (VM).

## Instalando pywiscat

Usa el instalador de paquetes de Python `pip3` para instalar pywiscat en tu VM:
```bash
pip3 install pywiscat
```

!!! note

    Si encuentras el siguiente error:

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Entonces ejecuta el siguiente comando:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...donde `$USER` es tu nombre de usuario en tu VM.

Verifica que la instalación fue exitosa:

```bash
pywiscat --version
```

## Encontrando datos con pywiscat

Por defecto, pywiscat se conecta al Global Discovery Catalogue (GDC) alojado por Environment and Climate Change Canada (ECCC).

!!! note "Cambiando la URL del GDC"
    Si estás realizando este ejercicio durante una sesión de formación local, puedes configurar pywiscat para consultar el GDC local estableciendo la variable de entorno `PYWISCAT_GDC_URL`:

    ```bash
    export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
    ```

Para ver las opciones disponibles, ejecuta:

```bash
pywiscat search --help
```

Puedes buscar en el GDC todos los registros:

```bash
pywiscat search
```

!!! question

    ¿Cuántos registros se devuelven de la búsqueda?

??? success "Haz clic para revelar la respuesta"
    El número de registros depende del GDC que estés consultando. Al usar el GDC de formación local, deberías ver que el número de registros es igual al número de conjuntos de datos que se han ingresado en el GDC durante las otras sesiones prácticas.

Probemos consultar el GDC con una palabra clave:

```bash
pywiscat search -q observations
```

!!! question

    ¿Cuál es la política de datos de los resultados?

??? success "Haz clic para revelar la respuesta"
    Todos los datos devueltos deberían especificar datos "core".

Prueba consultas adicionales con `-q`

!!! tip

    La bandera `-q` permite la siguiente sintaxis:

    - `-q synop`: encuentra todos los registros con la palabra "synop"
    - `-q temp`: encuentra todos los registros con la palabra "temp"
    - `-q "observations AND oman"`: encuentra todos los registros con las palabras "observations" y "oman"
    - `-q "observations NOT oman"`: encuentra todos los registros que contienen la palabra "observations" pero no la palabra "oman"
    - `-q "synop OR temp"`: encuentra todos los registros con "synop" o "temp"
    - `-q "obs*"`: búsqueda difusa

    Al buscar términos con espacios, encierra el término entre comillas dobles.

Obtengamos más detalles sobre un resultado de búsqueda específico que nos interese:

```bash
pywiscat get <id>
```

!!! tip

    Usa el valor de `id` del resultado de la búsqueda anterior.

## Conclusión

!!! success "¡Felicidades!"

    En esta sesión práctica, aprendiste a:

    - usar pywiscat para descubrir conjuntos de datos del WIS2 Global Discovery Catalogue