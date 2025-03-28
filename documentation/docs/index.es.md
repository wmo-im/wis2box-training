---
title: Inicio
---

<img alt="Logotipo de la OMM" src="../assets/img/wmo-logo.png" width="200">
# Entrenamiento de "WIS2-in-a-box"

"WIS2-in-a-box" ([wis2box](https://docs.wis2box.wis.wmo.int)) es una Implementación de Referencia de Código Abierto (FOSS) y gratuita de un Nodo WMO WIS2. El proyecto proporciona un conjunto de herramientas plug and play para ingerir, procesar y publicar datos meteorológicos/climáticos/hidrológicos utilizando enfoques basados en estándares alineados con los principios de WIS2. wis2box también proporciona acceso a todos los datos en la red de WIS2. wis2box está diseñado para tener una barrera de entrada baja para los proveedores de datos, ofreciendo infraestructura y servicios habilitadores para la búsqueda, acceso y visualización de datos.

Este entrenamiento proporciona explicaciones paso a paso de varios aspectos del proyecto wis2box, así como una serie de ejercicios para ayudarte a publicar y descargar datos de WIS2. El entrenamiento se proporciona en forma de presentaciones generales y también de ejercicios prácticos.

Los participantes podrán trabajar con datos de prueba y metadatos, así como integrar sus propios datos y metadatos.

Este entrenamiento cubre una amplia gama de temas (instalación/configuración, publicación/descarga de datos, etc.).

## Objetivos y resultados de aprendizaje

Los objetivos de este entrenamiento son familiarizarse con lo siguiente:

- Conceptos y componentes centrales de la arquitectura de WIS2
- Formatos de datos y metadatos utilizados en WIS2 para descubrimiento y acceso
- Arquitectura y entorno de wis2box
- Funciones principales de wis2box:
    - Gestión de metadatos
    - Ingesta de datos y transformación al formato BUFR
    - Broker MQTT para la publicación de mensajes de WIS2
    - Punto final HTTP para descarga de datos
    - Punto final de API para acceso programático a datos

## Navegación

La navegación a la izquierda proporciona una tabla de contenido para todo el entrenamiento.

La navegación a la derecha proporciona una tabla de contenido para una página específica.

## Requisitos previos

### Conocimientos

- Comandos básicos de Linux (consulta la [hoja de trucos](cheatsheets/linux.md))
- Conocimientos básicos de redes y protocolos de Internet

### Software

Este entrenamiento requiere las siguientes herramientas:

- Una instancia que ejecute el sistema operativo Ubuntu (proporcionado por los instructores de la OMM durante las sesiones de entrenamiento locales) consulta [Accediendo a tu VM de estudiante](practical-sessions/accessing-your-student-vm.md#introduction)
- Cliente SSH para acceder a tu instancia
- Explorador MQTT en tu máquina local
- Cliente SCP y FTP para copiar archivos desde tu máquina local

## Convenciones

!!! question

    Una sección marcada de esta manera te invita a responder una pregunta.

También notarás secciones de consejos y notas dentro del texto:

!!! tip

    Los consejos ofrecen ayuda sobre cómo lograr mejor las tareas.

!!! note

    Las notas proporcionan información adicional sobre el tema cubierto por la sesión práctica, así como la mejor manera de lograr tareas.

Los ejemplos se indican de la siguiente manera:

Configuración
``` {.yaml linenums="1"}
mi-colección-definida-en-yaml:
    type: collection
    title: mi título definido como un atributo yaml llamado title
    description: mi descripción como un atributo yaml llamado description
```

Fragmentos que deben escribirse en una terminal/consola se indican como:

```bash
echo 'Hello world'
```

Los nombres de los contenedores (imágenes en ejecución) se indican en **negrita**.

## Ubicación y materiales de entrenamiento

Los contenidos del entrenamiento, la wiki y el rastreador de problemas son gestionados en GitHub en [https://github.com/World-Meteorological-Organization/wis2box-training](https://github.com/World-Meteorological-Organization/wis2box-training).

## Imprimir el material

Este entrenamiento se puede exportar a PDF. Para guardar o imprimir este material de entrenamiento, ve a la [página de impresión](print_page) y selecciona Archivo > Imprimir > Guardar como PDF.

## Materiales de ejercicio

Los materiales de ejercicio se pueden descargar desde el archivo [exercise-materials.zip](/exercise-materials.zip) zipfile.

## Soporte

Para problemas/errores/sugerencias o mejoras/contribuciones a este entrenamiento, utiliza el [rastreador de problemas de GitHub](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

Todos los errores, mejoras y problemas de wis2box se pueden reportar en [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues).

Para soporte adicional o preguntas, por favor contacta a wis@wmo.int.

Como siempre, la documentación principal de wis2box siempre se puede encontrar en [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

¡Las contribuciones siempre son alentadas y bienvenidas!

