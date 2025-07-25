---
title: Inicio
---

<img alt="WMO logo" src="/assets/img/wmo-logo.png" width="200">
# Capacitación en WIS2 in a box

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) es una Implementación de Referencia de Código Abierto y Libre (FOSS) de un WMO WIS2 Node. El proyecto proporciona un conjunto de herramientas plug and play para ingerir, procesar y publicar datos de clima/meteorología/agua utilizando enfoques basados en estándares, en alineación con los principios de WIS2. wis2box también proporciona acceso a todos los datos en la red WIS2. wis2box está diseñado para tener una baja barrera de entrada para los proveedores de datos, proporcionando infraestructura y servicios habilitadores para el descubrimiento, acceso y visualización de datos.

Esta capacitación ofrece explicaciones paso a paso de varios aspectos del proyecto wis2box, así como una serie de ejercicios para ayudarte a publicar y descargar datos de WIS2. La capacitación se presenta en forma de presentaciones generales, así como ejercicios prácticos.

Los participantes podrán trabajar con datos y metadatos de prueba, así como integrar sus propios datos y metadatos.

Esta capacitación cubre una amplia gama de temas (instalación/configuración, publicación/descarga de datos, etc.).

## Objetivos y resultados de aprendizaje

Los objetivos de esta capacitación son familiarizarse con lo siguiente:

- Conceptos y componentes principales de la arquitectura WIS2
- Formatos de datos y metadatos utilizados en WIS2 para descubrimiento y acceso
- Arquitectura y entorno de wis2box
- Funciones principales de wis2box:
    - Gestión de metadatos
    - Ingesta de datos y transformación al formato BUFR
    - Broker MQTT para la publicación de mensajes WIS2
    - Endpoint HTTP para la descarga de datos
    - Endpoint API para el acceso programático a los datos

## Navegación

La navegación en el lado izquierdo proporciona una tabla de contenidos para toda la capacitación.

La navegación en el lado derecho proporciona una tabla de contenidos para una página específica.

## Requisitos previos

### Conocimientos

- Comandos básicos de Linux (consulta el [cheatsheet](./cheatsheets/linux.md))
- Conocimientos básicos de redes y protocolos de Internet

### Software

Esta capacitación requiere las siguientes herramientas:

- Una instancia que ejecute el sistema operativo Ubuntu (proporcionada por los instructores de la OMM durante las sesiones de capacitación locales) consulta [Accediendo a tu máquina virtual de estudiante](./practical-sessions/accessing-your-student-vm.md#introduction)
- Cliente SSH para acceder a tu instancia
- MQTT Explorer en tu máquina local
- Cliente SCP y SFTP para copiar archivos desde tu máquina local

## Convenciones

!!! question

    Una sección marcada de esta manera te invita a responder una pregunta.

También notarás secciones de consejos y notas dentro del texto:

!!! tip

    Los consejos ofrecen ayuda sobre cómo realizar mejor las tareas.

!!! note

    Las notas proporcionan información adicional sobre el tema cubierto en la sesión práctica, así como sobre cómo realizar mejor las tareas.

Los ejemplos se indican de la siguiente manera:

Configuración
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

Fragmentos que deben escribirse en un terminal/console se indican como:

```bash
echo 'Hello world'
```

Los nombres de los contenedores (imágenes en ejecución) se denotan en **negrita**.

## Ubicación y materiales de la capacitación

Los contenidos de la capacitación, el wiki y el rastreador de problemas se gestionan en GitHub en [https://github.com/wmo-im/wis2box-training](https://github.com/wmo-im/wis2box-training).

## Materiales de los ejercicios

Los materiales de los ejercicios pueden descargarse desde el archivo zip [exercise-materials.zip](/exercise-materials.zip).

## Soporte

Para problemas/errores/sugerencias o mejoras/contribuciones a esta capacitación, utiliza el [rastreador de problemas de GitHub](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

Todos los errores, mejoras y problemas de wis2box pueden reportarse en [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues).

Para soporte adicional o preguntas, contacta a wis2-support@wmo.int.

Como siempre, la documentación principal de wis2box se puede encontrar en [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

¡Las contribuciones siempre son bienvenidas y alentadas!