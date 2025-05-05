---
title: Descubriendo conjuntos de datos desde el WIS2 Global Discovery Catalogue
---

# Descubriendo conjuntos de datos desde el WIS2 Global Discovery Catalogue

!!! abstract "¡Resultados del aprendizaje!"

    Al final de esta sesión práctica, podrás:

    - usar pywiscat para descubrir conjuntos de datos desde el Global Discovery Catalogue (GDC)

## Introducción

En esta sesión aprenderás cómo descubrir datos desde el WIS2 Global Discovery Catalogue (GDC).

Actualmente, los siguientes GDCs están disponibles:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration: <https://gdc.wis.cma.cn>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc>

Durante las sesiones de capacitación local, se configura un GDC local para permitir que los participantes consulten el GDC para los metadatos que publicaron desde sus instancias de wis2box. En este caso, los instructores proporcionarán la URL al GDC local.

## Preparación

!!! note
    Antes de comenzar, por favor inicia sesión en tu máquina virtual de estudiante.

## Instalando pywiscat

Usa el instalador de paquetes Python `pip3` para instalar pywiscat en tu máquina virtual:
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

    ...donde `$USER` es tu nombre de usuario en tu máquina virtual.

Verifica que la instalación fue exitosa:

```bash
pywiscat --version
```

## Encontrando datos con pywiscat

Por defecto, pywiscat se conecta al Global Discovery Catalogue de Canadá. Vamos a configurar pywiscat para consultar el GDC de entrenamiento estableciendo la variable de entorno `PYWISCAT_GDC_URL`:

```bash
export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
```

Usemos [pywiscat](https://github.com/wmo-im/pywiscat) para consultar el GDC configurado como parte del entrenamiento.

```bash
pywiscat search --help
```

Ahora busca en el GDC todos los registros:

```bash
pywiscat search
```

!!! question

    ¿Cuántos registros se devuelven de la búsqueda?

??? success "Haz clic para revelar la respuesta"
    El número de registros depende del GDC que estés consultando. Cuando uses el GDC local de entrenamiento, deberías ver que el número de registros es igual al número de conjuntos de datos que se han ingresado en el GDC durante las otras sesiones prácticas.

Intentemos consultar el GDC con una palabra clave:

```bash
pywiscat search -q observations
```

!!! question

    ¿Cuál es la política de datos de los resultados?

??? success "Haz clic para revelar la respuesta"
    Todos los datos devueltos deberían especificar datos "core"

Prueba consultas adicionales con `-q`

!!! tip

    La bandera `-q` permite la siguiente sintaxis:

    - `-q synop`: encuentra todos los registros con la palabra "synop"
    - `-q temp`: encuentra todos los registros con la palabra "temp"
    - `-q "observations AND oman"`: encuentra todos los registros con las palabras "observations" y "oman"
    - `-q "observations NOT oman"`: encuentra todos los registros que contienen la palabra "observations" pero no la palabra "oman"
    - `-q "synop OR temp"`: encuentra todos los registros con "synop" o "temp"
    - `-q "obs*"`: búsqueda aproximada

    Cuando busques términos con espacios, enciérralos entre comillas dobles.

Obtengamos más detalles sobre un resultado de búsqueda específico que nos interese:

```bash
pywiscat get <id>
```

!!! tip

    Usa el valor `id` de la búsqueda anterior.

## Conclusión

!!! success "¡Felicitaciones!"

    En esta sesión práctica, aprendiste cómo:

    - usar pywiscat para descubrir conjuntos de datos desde el WIS2 Global Discovery Catalogue