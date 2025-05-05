---
title: Inicio
---

<img alt="WMO logo" src="../assets/img/wmo-logo.png" width="200">
# Capacitación WIS2 in a box

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) es una Implementación de Referencia Gratuita y de Código Abierto (FOSS) de un WMO WIS2 Node. El proyecto proporciona un conjunto de herramientas plug and play para ingerir, procesar y publicar datos meteorológicos/climáticos/hídricos utilizando enfoques basados en estándares alineados con los principios de WIS2. wis2box también proporciona acceso a todos los datos en la red WIS2. wis2box está diseñado para tener una baja barrera de entrada para los proveedores de datos, proporcionando infraestructura y servicios habilitadores para el descubrimiento, acceso y visualización de datos.

Esta capacitación proporciona explicaciones paso a paso de varios aspectos del proyecto wis2box, así como varios ejercicios para ayudarte a publicar y descargar datos de WIS2. La capacitación se proporciona en forma de presentaciones generales y ejercicios prácticos.

Los participantes podrán trabajar con datos y metadatos de prueba de muestra, así como integrar sus propios datos y metadatos.

Esta capacitación cubre una amplia gama de temas (instalación/configuración/ajustes, publicación/descarga de datos, etc.).

## Objetivos y resultados de aprendizaje

Los objetivos de esta capacitación son familiarizarse con lo siguiente:

- Conceptos básicos y componentes de la arquitectura WIS2
- Formatos de datos y metadatos utilizados en WIS2 para descubrimiento y acceso
- Arquitectura y entorno de wis2box
- Funciones principales de wis2box:
    - Gestión de metadatos
    - Ingesta de datos y transformación al formato BUFR
    - Broker MQTT para la publicación de mensajes WIS2
    - Punto final HTTP para descarga de datos
    - Punto final API para acceso programático a datos

## Navegación

La navegación del lado izquierdo proporciona una tabla de contenidos para toda la capacitación.

La navegación del lado derecho proporciona una tabla de contenidos para una página específica.

## Prerrequisitos

### Conocimientos

- Comandos básicos de Linux (ver la [guía de referencia](cheatsheets/linux.md))
- Conocimiento básico de redes y protocolos de Internet

### Software

Esta capacitación requiere las siguientes herramientas:

- Una instancia ejecutando sistema operativo Ubuntu (proporcionada por los instructores de WMO durante las sesiones de capacitación locales) ver [Accediendo a tu VM de estudiante](practical-sessions/accessing-your-student-vm.md#introduction)
- Cliente SSH para acceder a tu instancia
- MQTT Explorer en tu máquina local
- Cliente SCP y SFTP para copiar archivos desde tu máquina local

## Convenciones

!!! question

    Una sección marcada así te invita a responder una pregunta.

También notarás secciones de consejos y notas dentro del texto:

!!! tip

    Los consejos comparten ayuda sobre cómo lograr mejor las tareas.

!!! note

    Las notas proporcionan información adicional sobre el tema cubierto por la sesión práctica, así como la mejor manera de lograr las tareas.

Los ejemplos se indican de la siguiente manera:

Configuración
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

Los fragmentos que deben escribirse en una terminal/consola se indican como:

```bash
echo 'Hello world'
```

Los nombres de contenedores (imágenes en ejecución) se denotan en **negrita**.

## Ubicación y materiales de capacitación

Los contenidos de la capacitación, wiki y seguimiento de problemas se gestionan en GitHub en [https://github.com/World-Meteorological-Organization/wis2box-training](https://github.com/World-Meteorological-Organization/wis2box-training).

## Impresión del material

Esta capacitación puede exportarse a PDF. Para guardar o imprimir este material de capacitación, ve a la [página de impresión](print_page), y selecciona
Archivo > Imprimir > Guardar como PDF.

## Materiales de ejercicios

Los materiales de ejercicios se pueden descargar desde el archivo [exercise-materials.zip](/exercise-materials.zip).

## Soporte

Para problemas/errores/sugerencias o mejoras/contribuciones a esta capacitación, utiliza el [seguimiento de problemas de GitHub](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

Todos los errores, mejoras y problemas de wis2box pueden reportarse en [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues).

Para soporte adicional o preguntas, contacta a wis2-support@wmo.int.

Como siempre, la documentación principal de wis2box puede encontrarse en [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

¡Las contribuciones siempre son alentadas y bienvenidas!