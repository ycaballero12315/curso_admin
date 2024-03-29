import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Función para convertir el tamaño del archivo a MB
def convertir_a_mb(size):
    return size / (1024 * 1024)

# Función para enviar correo electrónico
def enviar_correo(destinatario, asunto, cuerpo):
    # Configurar conexión SMTP
    servidor_smtp = smtplib.SMTP('smtp.example.com', 587)  # Coloca tu servidor SMTP y puerto
    servidor_smtp.starttls()
    servidor_smtp.login('tu_correo@example.com', 'tu_contraseña')  # Coloca tu dirección de correo y contraseña

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = 'tu_correo@example.com'  # Coloca tu dirección de correo
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    # Adjuntar el cuerpo del mensaje
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Enviar el correo
    servidor_smtp.send_message(mensaje)

    # Cerrar conexión SMTP
    servidor_smtp.quit()

# Directorio a analizar
directorio = input("Ingrese el directorio a analizar: ")

# Obtener la lista de archivos
result = subprocess.check_output(["find", directorio, "-type", "f"]).decode().splitlines()

# Diccionario para almacenar la suma de los tamaños de archivo por propietario
propietarios = {}

# Calcular el tamaño total de archivos por propietario
for file in result:
    owner = os.stat(file).st_uid
    size = os.stat(file).st_size
    size_mb = convertir_a_mb(size)
    propietarios[owner] = propietarios.get(owner, 0) + size_mb

# Construir el cuerpo del mensaje del correo
cuerpo = ""
for owner, total_size in propietarios.items():
    # Concatenar el destinatario con @refcfg.cu
    destinatario = f"{owner}@refcfg.cu"
    # Obtener el nombre del propietario a partir del ID de usuario
    propietario_nombre = subprocess.check_output(["getent", "passwd", str(owner)]).decode().split(':')[4]
    asunto = f"Archivos en {directorio}"
    cuerpo += f"Propietario: {propietario_nombre}\n"
    cuerpo += f"Tamaño total de archivos: {total_size:.2f} MB\n\n"

# Enviar el correo electrónico
enviar_correo(destinatario, asunto, cuerpo)

print("Correo electrónico enviado correctamente.")
