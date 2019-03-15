# Meli Drive Challenge

Esta app utiliza las credenciales de usuario de Google para hacer un relevamiento de los archivos almacenados en su drive. Al mismo tiempo, almacena localmente en una instancia de MySQL dicha información. Adicionalmente este modifica los archivos y carpetas que tengan visibilidad Pública del Drive a Privada. Luego de realizar dicho cambio, utiliza las credenciales del usuario para notificar a los dueños de ese/a archivo/carpeta.

## Empezando

El siguiente comando creará una copia del repositorio de GitHub en el directorio en que esté situado:
```
$ git clone https://username@github.com/lucianosebastianelli/meli_drive_challenge
``` 
Una vez copiado el repositorio, ejecute la app con el siguiente comando:
```
$ python3 main.py LOCALHOST DB_NAME USER -p PASSWORD
```
CAMPOS OBLIGATORIOS:
* LOCALHOST: host de la conexión a mySQL (ej: localhost)
* DB_NAME: nombre de la base de datos 
* USER: nombre de usuario de la base de datos (ej: root)

CAMPOS OPCIONALES:
* PASSWORD: contraseña de la base de datos

Para más información ejecute el siguiente comando:
```
$ python3 main.py -h
```

### Requisitos

Este proyecto requiere:
  * Versión de python 3 o sup.
  * Instancia de MySQL Server instalada.
  * Instalar Google Drive API y Google Mail API para python.

```
https://www.python.org/download/releases/3.0/
https://dev.mysql.com/downloads/mysql/
https://developers.google.com/drive/api/v3/quickstart/python
https://developers.google.com/gmail/api/quickstart/python

```

## Notas de versión v1.0

Las API's de Google presentan algunas inconsistencias con lo documentado en el sitio [Google Developers](https://developers.google.com/gmail/). Según se investigó, la API de GMail no funciona correctamente al intentar enviar mails. El código posee avisos customizados que indicarán cómo poder simular su correcto funcionamiento.

## Autor

**Luciano Sebastianelli** - *desarrollador de la solución* - [My Repositorio](https://github.com/lucianosebastianelli)

## Fuentes

* [Stack Overflow](https://stackoverflow.com/): extensa comunidad de desarrolladores donde se encuentra todo tipo de ayuda en lenguajes de programación. *(consultados: comandos de Python, MySQL, linux y errores en general.)*
* [PYNative](https://pynative.com/): comunidad avocada a tutoriales y procedimientos en lenguaje Python. *(consultados: Manejar conexiones y cursores a MySQL, commits, rollbacks, error handling, etc.)*
* [GitHub](https://github.com/): comunidad de desarrolladores que comparten código abierto y responden consultas. *(consultados: problemas con API's de Google y errores en general.)*
* [Google Developers](https://developers.google.com/): página oficial de soporte a las API's de Google con tutoriales y ejemplos de aplicación en distintas plataformas. *(consultados: instalación e implementación general de las API's.)*
* Conocimientos previos en paradigmas de programación funcional y de objetos.

