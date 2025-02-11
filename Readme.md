# Documentación del Proyecto

## Descripción
Este proyecto se encarga de integrar varias funcionalidades de un sistema de torneos, incluyendo la gestión de torneos, participantes, juegos y equipos, mediante la interacción con una API externa. Los datos se obtienen mediante solicitudes HTTP a la API y se muestran en plantillas HTML renderizadas en Django.

## Estructura de Archivos

- **views.py**: Contiene las vistas que manejan la lógica de la aplicación y la interacción con la API externa.
- **.env**: Archivo donde se almacenan las variables de entorno (como claves de acceso) que no deben ser hardcodeadas.
- **templates/**: Carpeta que contiene las plantillas HTML donde se visualizan los datos obtenidos de la API.

---

## **Flujo de Funcionalidad**

### 1. **Configuración de Variables de Entorno**

En el archivo `.env` se deben definir las siguientes claves:

- **USER_KEY_ADMINISTRADOR**: Clave de API para el administrador.
- **USER_KEY_JUGADOR**: Clave de API para el jugador.
- **USER_KEY_ORGANIZADOR**: Clave de API para el organizador.

Esto permite una gestión segura de las claves sin necesidad de incluirlas directamente en el código.

---

### 2. **Vistas y Funciones**g

#### **Vistas Principales**

Las vistas están diseñadas para interactuar con la API externa y mostrar los datos en plantillas HTML.

# Respuestas a las preguntas

1. **Por cada petición que hemos hecho, se ha incluido siempre lo siguiente: `http://127.0.0.1:8000/api/v1/libros/`, ¿qué pasaría si en un futuro, la versión cambia? ¿Deberíamos cambiarlo en todos los sitios de la aplicación? ¿Cómo podríamos mejorarlo?**

   Si en el futuro la versión de la API cambia, tendríamos que actualizar todas las URLs en el código, lo cual es un problema estar cambiandolo constantemenete. Para evitar esto, lo mejor es definir la versión de la API en una variable y usar esa variable en todas las peticiones. Así, si la versión cambia, solo tenemos que actualizar la variable en un solo lugar. En el código, ya hemos hecho esto definiendo `API_VERSION` y `API_BASE_URL`.

2. **Para la respuesta siempre incluimos la misma línea: `response.json()`. ¿Qué pasaría si en el día de mañana cambia el formato en una nueva versión, y en vez de json es xml? ¿Debemos volver a cambiar en todos los sitios esa línea?**

   Si el formato de la respuesta cambia de JSON a XML, tendríamos que cambiar `response.json()` en todos los lugares donde lo usamos. Para evitar esto, hemos creado una función `process_response` que maneja diferentes formatos de respuesta. Así, si el formato cambia, solo necesitamos actualizar esa función.

3. **¿Siempre debemos tratar todos los errores en cada una de las peticiones?**

   No, no siempre es necesario tratar todos los errores en cada petición. Sin embargo, es una buena práctica manejar los errores comunes y tener una función general para tratar errores específicos. En el código, hemos implementado funciones como `tratar_errores`, `mi_error_404`, y `mi_error_500` para manejar errores de manera centralizada.


Invoke-WebRequest -Uri "http://127.0.0.1:8000/oauth2/token/" `
                  -Method POST `
                  -Body "grant_type=password&username=javier&password=elpepe34&client_id=loloid&client_secret=lolosecreto" `

Invoke-WebRequest -Uri "http://127.0.0.1:8000/oauth2/token/" `
                  -Method POST `
                  -Body "grant_type=password&username=admin&password=admin&client_id=pepeid&client_secret=pepesecreto" `
                  -ContentType "application/x-www-form-urlencoded"