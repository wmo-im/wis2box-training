---
title: Descargando con WIS2 Downloader
---

# Descargando con WIS2 Downloader

!!! abstract "¡Resultados de aprendizaje!"

    Al final de esta sesión práctica, podrás:

    - encontrar y suscribirte a conjuntos de datos
    - usar filtros para controlar los archivos descargados
    - utilizar autenticación para descargar conjuntos de datos con acceso controlado
    - cambiar la configuración predeterminada de WIS2 Downloader para casos de uso más avanzados

## Introducción

En WIS2, todos los conjuntos de datos tienen un archivo de metadatos que se puede encontrar en los **Global Discovery Catalogues**. Por lo tanto, se espera que los usuarios consulten siempre estos servicios para encontrar los datos compartidos en WIS2.

WIS2 Downloader utiliza este principio al buscar todos los registros disponibles en estos GDCs y combinarlos internamente para permitir al usuario navegar por los datos disponibles en WIS2. Dado que hay una gran cantidad de registros para mostrar, es esencial proporcionar una forma para que el usuario los filtre y encuentre el registro correcto. Incluso después de encontrar y suscribirse al registro correcto, puede haber conjuntos de datos donde el número de archivos exceda las necesidades actuales del usuario. Debido a esto, se necesita un segundo nivel de filtrado, uno que opere en el momento de decidir si un archivo debe descargarse.

## Uso en la Vista de Catálogo

La **Vista de Catálogo** es una de las dos formas de encontrar y suscribirse a conjuntos de datos en WIS2 Downloader. Agrega registros de los Global Discovery Catalogues y los presenta en una interfaz que se puede buscar y filtrar, similar a navegar directamente por un portal GDC.

Navega a **Vista de Catálogo** en la barra lateral izquierda.

![WIS2 Downloader Catalogue View](../assets/img/wis2-downloader-catalogue-view.png)

En la parte superior de la página encontrarás una barra de búsqueda y un conjunto de filtros. Puedes utilizarlos para reducir la lista de registros disponibles por palabra clave, Centre ID o política de datos (core vs. recommended).

También puedes filtrar espacialmente definiendo un **bounding box** utilizando cuatro entradas de coordenadas: **North**, **West**, **South** y **East**, expresadas como valores decimales de latitud y longitud. Cuando se establece un bounding box, puedes elegir entre dos modos de coincidencia:

- **Intersects** — devuelve registros cuyo alcance espacial se superpone con el bounding box de cualquier manera.
- **Within** — devuelve solo registros cuyo alcance espacial cae completamente dentro del bounding box.

!!! note "Recargar el catálogo"

    El catálogo se carga desde los GDCs cuando WIS2 Downloader se inicia. Si crees que la lista está desactualizada, puedes forzar una recarga desde la sección **Settings** en la barra lateral izquierda.

### Ejercicio: encontrar y suscribirse a un conjunto de datos

!!! question "Encontrar un conjunto de datos de observación de superficie"

    Utiliza los filtros en la Vista de Catálogo para encontrar un conjunto de datos de observación de superficie **core** relacionado con temperatura y precipitación.

    1. Escribe `surface` en la barra de búsqueda y observa cómo se filtra la lista de registros.
    2. Establece el filtro de política de datos en **core**.
    3. Configura las palabras clave para incluir `temperature, precipitation` y observa cómo cambian los resultados.
    4. Selecciona un registro de los resultados para expandir sus detalles.
    5. Revisa los metadatos mostrados: nota el tema, el centro de origen y la política de datos.
    6. Configura la carpeta de destino como `surface-obs`.
    7. Haz clic en **Subscribe** para crear la suscripción.

    Después de suscribirte, navega a **Manage Subscriptions** para confirmar que la nueva suscripción aparece en la lista.

??? success "Haz clic para revelar la respuesta"

    Cualquier registro cuyo tema contenga `surface-based-observations` y cuya política de datos sea `core` es una elección válida. Aplicar el filtro de palabras clave para `temperature, precipitation` reducirá aún más los resultados a conjuntos de datos relevantes para esas variables.

    Una vez suscrito, la vista **Manage Subscriptions** mostrará la suscripción activa con su tema y carpeta de destino. Los archivos comenzarán a descargarse a medida que lleguen nuevas notificaciones al broker.

!!! note "Cancelar suscripción y eliminar archivos descargados"
    
    Ve a la vista **Manage Subscriptions** y selecciona `Unsubscribe` del tema elegido en el ejercicio anterior.

    Luego, limpia la carpeta de descargas:

    ```bash
    rm -fr /home/<username>/wis2-downloads/surface-obs
    ```

## Uso de la Vista de Árbol

La **Vista de Árbol** presenta la jerarquía de temas de WIS2 como un árbol colapsable, permitiéndote explorar los temas disponibles nivel por nivel, similar a navegar por temas en MQTT Explorer. Está diseñada para una exploración de alto nivel y de arriba hacia abajo de los datos disponibles en WIS2, comenzando desde la raíz de la jerarquía y profundizando. Esto contrasta con la Vista de Catálogo, que te lleva directamente a registros individuales de conjuntos de datos y es más adecuada cuando ya sabes lo que estás buscando.

Navega a **Vista de Árbol** en la barra lateral izquierda.

![WIS2 Downloader Tree View](../assets/img/wis2-downloader-tree-view.png)

El árbol está organizado siguiendo la jerarquía de temas de WIS2. Expande cada nivel haciendo clic en un nodo para revelar sus hijos. En cualquier nivel puedes suscribirte seleccionando un nodo y haciendo clic en **Subscribe**, utilizando un comodín (`#`) para capturar todos los temas debajo de ese nodo.

!!! note "Suscribirse en diferentes niveles"

    Suscribirse más arriba en el árbol (por ejemplo, en el nivel de Centre ID) capturará todos los conjuntos de datos publicados por ese centro. Suscribirse más abajo te da un control más granular. Usa el sufijo comodín `#` que WIS2 Downloader agrega automáticamente al suscribirse desde la Vista de Árbol.

### Ejercicio: encontrar y suscribirse usando la Vista de Árbol

!!! question "Suscribirse a un conjunto de datos mediante la Vista de Árbol"

    Utiliza la Vista de Árbol para encontrar y suscribirte a datos de observación de superficie de un centro específico.

    1. Expande el árbol comenzando desde el nodo `cache`, luego navega a través de `a` → `wis2`.
    2. Selecciona un Centre ID de tu elección y continúa expandiendo hasta que llegues a un tema relacionado con `surface-based-observations`.
    3. Revisa la ruta completa del tema mostrada: confirma que corresponde al conjunto de datos que deseas.
    4. Configura la carpeta de destino como `surface-obs-tree`.
    5. Haz clic en **Subscribe** para crear la suscripción.

    Navega a **Manage Subscriptions** para confirmar que la suscripción está activa.

??? success "Haz clic para revelar la respuesta"

    Cualquier ruta de tema que siga el patrón `cache/a/wis2/<centre-id>/data/core/weather/surface-based-observations/#` es una elección válida. El segmento de Centre ID variará dependiendo del centro que seleccionaste en el árbol.

    La vista **Manage Subscriptions** mostrará la nueva suscripción junto con cualquier otra creada previamente.

!!! note "Cancelar suscripción y eliminar archivos descargados"
    
    Ve a la vista **Manage Subscriptions** y selecciona `Unsubscribe` del tema elegido en el ejercicio anterior.

    Luego, limpia la carpeta de descargas:

    ```bash
    rm -fr /home/<username>/wis2-downloads/surface-obs-tree
    ```

## Uso de la Vista de Suscripción Manual

La vista **Manual Subscribe** te permite crear una suscripción ingresando directamente un tema, sin depender de los Global Discovery Catalogues. A diferencia de la Vista de Catálogo y la Vista de Árbol — que obtienen sus temas de los GDCs — Manual Subscribe es útil cuando ya conoces el tema exacto al que deseas suscribirte y quieres configurarlo sin navegar por el catálogo, con más libertad sobre el WTH que se utilizará.

Navega a **Manual Subscribe** en la barra lateral izquierda.

![WIS2 Downloader Manual Subscribe](../assets/img/wis2-downloader-manual-subscribe.png)

El formulario te permite especificar:

- **Topic** — el tema completo de MQTT al que suscribirse, incluidos los comodines (por ejemplo, `#` y `+`).
- **Destination folder** — el subdirectorio local donde se guardarán los archivos descargados.
- **Filter** — un objeto de filtro opcional en forma de texto para controlar qué notificaciones se descargan.
- **Priority queue** — controla la prioridad de descarga asignada a las notificaciones de esta suscripción.
- **Authentication** — credenciales requeridas para conjuntos de datos con acceso controlado.

!!! note "Cuándo usar Manual Subscribe"

    Usa Manual Subscribe cuando ya conoces el tema exacto que deseas y quieres configurarlo rápidamente sin navegar por el catálogo, cuando el tema no está incluido en el catálogo o cuando necesitas proporcionar credenciales para un conjunto de datos con acceso controlado.

## Descargando desde un conjunto de datos con acceso controlado

Algunos conjuntos de datos en WIS2 tienen acceso controlado, lo que significa que requieren credenciales válidas antes de que los archivos puedan descargarse. WIS2 Downloader admite dos métodos de autenticación en la vista Manual Subscribe:

- **Autenticación HTTP básica** — proporciona un nombre de usuario y contraseña asociados con tus credenciales de acceso.
- **Token Bearer** — proporciona un token emitido por el editor de datos en lugar de un nombre de usuario y contraseña.

Estas credenciales se almacenan por suscripción y se aplican automáticamente al descargar archivos para ese tema.

### Ejercicio: suscribirse a un conjunto de datos con acceso controlado en tu wis2box

En este ejercicio configurarás un conjunto de datos con acceso controlado en tu instancia de wis2box, configurarás WIS2 Downloader para suscribirte a su broker y verificarás que los archivos se descarguen correctamente cuando se proporcione un token bearer.

!!! question "Configurar y suscribirse a un conjunto de datos con acceso controlado"

    **Paso 1 — Crear un conjunto de datos con acceso controlado en wis2box**

    En tu instancia de wis2box, crea un conjunto de datos con control de acceso habilitado y toma nota del tema y del token bearer generado para él. Si aún no lo has hecho, consulta la sesión práctica [Datasets with access control](datasets-with-access-control.md) para los pasos completos de configuración.

**Paso 2 — Configurar WIS2 Downloader para escuchar al broker de wis2box**

Por defecto, WIS2 Downloader escucha al Global Broker. Para recibir notificaciones directamente desde tu instancia de wis2box, necesitas agregar un suscriptor en el archivo compose de WIS2 Downloader que apunte al broker interno MQTT de wis2box.

Abre el archivo `docker-compose.yml` en el directorio de WIS2 Downloader y agrega la siguiente configuración de suscriptor, reemplazando `WIS2BOX_URL` con la URL de tu instancia de wis2box:

```yaml
  subscriber-test:
container_name: subscriber-test
restart: always
build:
  context: .
  dockerfile: ./containers/subscriber/Dockerfile
  args:
    WIS2DOWNLOADER_UID: ${WIS2DOWNLOADER_UID:-10001}
    WIS2DOWNLOADER_GID: ${WIS2DOWNLOADER_GID:-988}
env_file: *default-env
environment:
  GLOBAL_BROKER_HOST: WIS2BOX_URL
  GLOBAL_BROKER_PORT: 443
  GLOBAL_BROKER_USERNAME: everyone
  GLOBAL_BROKER_PASSWORD: everyone
  MQTT_PROTOCOL: websockets
depends_on:
  - redis
networks:
  - redis-net
logging: *loki-logging
healthcheck:
  test: ["CMD", "pgrep", "-f", "subscriber_start"]
  interval: 30s
  timeout: 5s
  retries: 3
```

Reinicia el stack para aplicar los cambios:

```bash
docker compose down
docker compose up -d
```

**Paso 3 — Suscribirse al conjunto de datos en WIS2 Downloader**

1. Navega a **Manual Subscribe** en la interfaz de usuario de WIS2 Downloader.
2. Configura el tema al que está asociado tu conjunto de datos con control de acceso en wis2box.
3. Configura la carpeta de destino como `restricted-data`.
4. Ingresa el token bearer generado en el Paso 1 en el campo **Authentication**.
5. Haz clic en **Subscribe** para crear la suscripción.

**Paso 4 — Enviar datos al conjunto de datos en wis2box**

En tu instancia de wis2box, publica un archivo en el conjunto de datos con control de acceso. Consulta la sesión práctica [Ingesting data for publication](ingesting-data-for-publication.md) para los pasos sobre cómo ingresar datos.

**Paso 5 — Verificar la descarga**

Verifica que el archivo haya sido descargado por WIS2 Downloader:

```bash
ls /home/<username>/wis2-downloads/restricted-data
```

??? success "Haz clic para revelar la respuesta"

Con un token bearer válido, WIS2 Downloader se autentica al descargar archivos para el tema restringido. El archivo publicado en el Paso 4 debería aparecer en la carpeta `restricted-data` poco después de ser ingresado por wis2box.

Si la autenticación falla, los archivos no se descargarán aunque la suscripción aparezca activa en la vista **Manage Subscriptions**. Verifica que el token bearer coincida con el configurado en el conjunto de datos en wis2box.

!!! note "Cancelar suscripción y eliminar archivos descargados"

Ve a la vista **Manage Subscriptions** y haz clic en **Unsubscribe** del tema, luego limpia la carpeta de descargas:

```bash
rm -fr /home/<username>/wis2-downloads/restricted-data
```

## Filtrar descargas

Los filtros te permiten controlar qué archivos se descargan de una suscripción a nivel de notificación — este es el segundo nivel de filtrado mencionado en la introducción. En lugar de descargar cada archivo publicado en un tema, puedes definir un filtro para que solo las notificaciones que cumplan con criterios específicos desencadenen una descarga.

Después de seleccionar un conjunto de datos en la vista **Catalogue View** o **Tree View**, aparece un panel de filtros en el lado derecho de la pantalla antes de suscribirte. Aquí puedes completar los valores de filtro que deseas aplicar. WIS2 Downloader construye automáticamente el objeto de filtro a partir de tus entradas.

En la vista **Manual Subscribe**, deberías ingresar este objeto de filtro manualmente completando el campo `Filter (JSON)` en el formulario.

!!! note "Entradas de filtro disponibles"

- **Media type** — restringe las descargas a tipos de contenido específicos (por ejemplo, `application/bufr`).
- **Dataset** — restringe las descargas a un conjunto de datos específico mediante su identificador de metadatos.
- **Bounding box** — restringe las descargas a notificaciones cuyos datos caen dentro de un área espacial, definida por los valores `north`, `south`, `east` y `west`.
- **Date & time range** — restringe las descargas a notificaciones publicadas dentro de un rango de tiempo específico.
- **Custom filters** — filtra por cualquier otra propiedad de notificación definida en el registro de metadatos especificando el valor de la propiedad (por ejemplo, filtrando por `wigos_station_identifier` para descargar solo datos de una estación específica).

El siguiente es un ejemplo del objeto de filtro generado a partir de estas entradas:

```json
{
  "rules": [
    {
      "id": "accept",
      "order": 1,
      "match": {
        "all": [
          {
            "any": [
              { "media_type": { "exists": false } },
              { "media_type": { "in": ["application/bufr", "application/x-bufr"] } }
            ]
          },
          { "metadata_id": { "in": ["urn:wmo:md:ir-irimo:core.surface-based-observations.temp"] } },
          { "bbox": { "north": 23.0, "south": 27.0, "east": 25.0, "west": 28.0 } },
          {
            "property": "pubtime",
            "type": "datetime",
            "between": ["2026-06-08T20:00:00+00:00", "2026-06-09T05:00:59+00:00"]
          },
          {
            "property": "wigos_station_identifier",
            "type": "string",
            "in": ["0-20000-0-78338"]
          }
        ]
      },
      "action": "accept"
    },
    {
      "id": "default",
      "order": 999,
      "match": { "always": true },
      "action": "reject",
      "reason": "No filter criteria matched"
    }
  ]
}
```

### Ejercicio: Suscribirse con un filtro

Usa la vista Catalogue View para encontrar un conjunto de datos de observaciones superficiales y aplica un filtro espacial antes de suscribirte.

1. Navega a **Catalogue View** y busca un conjunto de datos de observaciones superficiales de tu elección.
2. Selecciona el conjunto de datos para expandir sus detalles en el panel derecho.
3. En las entradas de filtro, configura un **bounding box** para una región de tu elección.
4. Opcionalmente, configura un filtro de **media type** para restringir las descargas a archivos BUFR.
5. Configura la carpeta de destino como `filtered-obs`.
6. Haz clic en **Subscribe** para crear la suscripción.

Espera a que lleguen los archivos y verifica que solo se descarguen los archivos que cumplan con tus criterios de filtro.

??? success "Haz clic para revelar la respuesta"

Solo las notificaciones que cumplan con todas las condiciones que definiste serán aceptadas y descargadas. Todas las demás serán rechazadas por la regla predeterminada de rechazo.

!!! note "Cancelar suscripción y eliminar archivos descargados"

Ve a la vista **Manage Subscriptions** y haz clic en **Unsubscribe** del tema, luego limpia la carpeta de descargas:

```bash
rm -fr /home/<username>/wis2-downloads/filtered-obs
```

## Conclusión

!!! success "¡Felicidades!"

En esta sesión práctica, aprendiste a:

- encontrar y suscribirte a conjuntos de datos usando las vistas Catalogue View y Tree View
- suscribirte directamente a temas usando la vista Manual Subscribe
- aplicar filtros para controlar qué archivos se descargan de una suscripción
- usar autenticación para descargar conjuntos de datos con control de acceso