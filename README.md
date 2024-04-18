## Nombre del Proyecto

Título del Proyecto: Sistema de Monitoreo de Ficheros en FileServer del dominio refcfg.cu

## Resumen:

El Sistema de Monitoreo de Archivos es una herramienta diseñada para escanear y monitorear los archivos almacenados en servidores de datos de Refineria S.A, como ej (vs31.refcfg.cu, vs30.refcfg.cu o vs24.refcfg.cu). El objetivo principal del sistema es identificar y notificar a los propietarios de archivos que exceden un tamaño especificado por el admin de redes.
Características: 1. Escaneo de Archivos: El sistema permite al especialista de seguridad informatica especificar un directorio en el fileServer del dominio refcfg.cu y un tamaño límite en megabytes. Luego, escanea los archivos en el directorio proporcionado y genera una lista de archivos que exceden el tamaño especificado. 2. Generación de Informes: Con la información recopilada durante el escaneo, el sistema crea un informe detallado que incluye el nombre del archivo, el directorio donde se encuentra, el tamaño del archivo, el tipo de archivo y el propietario del mismo. 3. Almacenamiento en Formato TXT y JSON: El sistema guarda el informe generado en dos formatos: un archivo de texto (.txt) para revision offline por el especialista o administrativo interesado o el propio usuario y un archivo JSON (.json). Estos archivos se almacenan localmente para su posterior consulta o análisis. 4. Notificación por Correo Electrónico: Utilizando los datos recopilados en el informe JSON, el sistema envía notificaciones por correo electrónico a los propietarios de los archivos que exceden el tamaño especificado. Las notificaciones incluyen información relevante sobre los archivos y una advertencia sobre el uso del espacio en disco, exisge al usuario su eleiminacion del server por problema de espacio.
Beneficios:
• Facilita la identificación de archivos que ocupan un espacio considerable en el servidor de dominio refcfg.cu, ayudando asi a que se haga un uso adecuado del espacio de los server de salva de informacion.
• Ayuda a los propietarios de archivos a gestionar el espacio en disco de manera más eficiente.
• Proporciona una solución automatizada para monitorear y notificar sobre el uso excesivo de espacio en disco en los servidores de ficheros del dominio refcfg.
El Sistema de Monitoreo de Archivos en los FileServer del Dominio refcfg.cu es una herramienta útil para administradores de sistemas y los especialistas de seguridad informatica que necesitan mantener un control efectivo sobre el uso de espacio en disco en entornos empresariales.

## Instalacion

git clone https://github.com/ycaballero12315/curso_admin.git

## Configuracion

Crear la carpeta env dentro config.py con las variables de entorno

# Uso

# Scan

python3 main.py

# send mail

python3 sendmail.py
