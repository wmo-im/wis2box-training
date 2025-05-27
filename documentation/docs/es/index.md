---
title: Inicio
---

<img alt="Logo de la OMM" src="/assets/img/wmo-logo.png" width="200">
# Capacitación de WIS2 in a box

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) es una Implementación de Referencia de Código Abierto y Gratuita de un Nodo WIS2 de la OMM. El proyecto proporciona un conjunto de herramientas plug and play para ingerir, procesar y publicar datos de clima, agua y meteorología utilizando enfoques basados en estándares alineados con los principios de WIS2. wis2box también proporciona acceso a todos los datos en la red WIS2. wis2box está diseñado para tener una baja barrera de entrada para los proveedores de datos, proporcionando infraestructura y servicios habilitantes para el descubrimiento, acceso y visualización de datos.

Esta capacitación proporciona explicaciones paso a paso de varios aspectos del proyecto wis2box, así como una serie de ejercicios para ayudarte a publicar y descargar datos de WIS2. La capacitación se ofrece en forma de presentaciones generales y ejercicios prácticos.

Los participantes podrán trabajar con datos de prueba y metadatos de muestra, así como integrar sus propios datos y metadatos.

Esta capacitación cubre una amplia gama de temas (instalación/configuración/configuración, publicación/descarga de datos, etc.).

## Objetivos y resultados de aprendizaje

Los objetivos de esta capacitación son familiarizarse con lo siguiente:

- Conceptos y componentes centrales de la arquitectura de WIS2
- Formatos de datos y metadatos utilizados en WIS2 para descubrimiento y acceso
- Arquitectura y entorno de wis2box
- Funciones principales de wis2box:
    - gestión de metadatos
    - ingestión de datos y transformación al formato BUFR
    - broker MQTT para la publicación de mensajes de WIS2
    - Punto final HTTP para la descarga de datos
    - Punto final de API para acceso programático a los datos

## Navegación

La navegación de la mano izquierda proporciona una tabla de contenidos para toda la capacitación.

La navegación de la mano derecha proporciona una tabla de contenidos para una página específica.

## Prerrequisitos

### Conocimientos

- Comandos básicos de Linux (ver la [cheatsheet](./cheatsheets/linux.md))
- Conocimientos básicos de redes y protocolos de Internet

### Software

Esta capacitación requiere las siguientes herramientas:

- Una instancia ejecutando el sistema operativo Ubuntu (proporcionada por los entrenadores de la OMM durante las sesiones de capacitación locales) ver [Accediendo a tu VM de estudiante](./practical-sessions/accessing-your-student-vm.md#introduction)
- Cliente SSH para acceder a tu instancia
- MQTT Explorer en tu máquina local
- Cliente SCP y SFTP para copiar archivos desde tu máquina local

## Convenciones

!!! question

    Una sección marcada de esta manera te invita a responder una pregunta.

También notarás secciones de consejos y notas dentro del texto:

!!! tip

    Los consejos comparten ayuda sobre cómo lograr mejor las tareas.

!!! note

    Las notas proporcionan información adicional sobre el tema cubierto por la sesión práctica, así como cómo lograr mejor las tareas.

Los ejemplos se indican de la siguiente manera:

Configuración
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

Los fragmentos que necesitan ser escritos en un terminal/consola se indican como:

```bash
echo 'Hello world'
```

Los nombres de contenedores (imágenes en ejecución) se denotan en **negrita**.

## Ubicación y materiales de la capacitación

Los contenidos de la capacitación, el wiki y el rastreador de problemas se gestionan en GitHub en [https://github.com/World-Meteorological-Organization/wis2box-training](https://github.com/World-Meteorological-Organization/wis2box-training).

## Imprimiendo el material

Esta capacitación puede ser exportada a PDF. Para guardar o imprimir este material de capacitación, ve a la [página de impresión](./print_page/), y selecciona
Archivo > Imprimir > Guardar como PDF.

## Materiales de los ejercicios

Los materiales de los ejercicios se pueden descargar desde el archivo [exercise-materials.zip](/exercise-materials.zip).

## Soporte

Para problemas/bugs/sugerencias o mejoras/contribuciones a esta capacitación, por favor usa el [rastreador de problemas de GitHub](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

Todos los bugs, mejoras y problemas de wis2box pueden ser reportados en [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues).

Para soporte adicional o preguntas, por favor contacta a wis2-support@wmo.int.

Como siempre, la documentación principal de wis2box siempre se puede encontrar en [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

¡Las contribuciones siempre son alentadas y bienvenidas!