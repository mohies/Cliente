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

### 2. **Vistas y Funciones**

#### **Vistas Principales**

Las vistas están diseñadas para interactuar con la API externa y mostrar los datos en plantillas HTML.
