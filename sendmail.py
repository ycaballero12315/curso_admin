import json
import smtplib
from email.mime.text import MIMEText

# Función para enviar correo electrónico
def enviar_correo(destinatario, mensaje):
    # Configurar servidor SMTP
    servidor_smtp = 'smtp.gmail.com'
    puerto_smtp = 587
    usuario = 'tucorreo@gmail.com'
    contraseña = 'tupassword'

    # Configurar mensaje
    msg = MIMEText(mensaje)
    msg['From'] = usuario
    msg['To'] = destinatario
    msg['Subject'] = 'Correo de notificación'

    # Iniciar conexión SMTP
    server = smtplib.SMTP(servidor_smtp, puerto_smtp)
    server.starttls()
    server.login(usuario, contraseña)

    # Enviar correo electrónico
    server.sendmail(usuario, destinatario, msg.as_string())

    # Cerrar conexión SMTP
    server.quit()

# Leer archivo JSON
with open('propietarios.json') as f:
    datos = json.load(f)

# Iterar sobre los propietarios y enviar correo electrónico
for propietario in datos:
    destinatario = propietario['propietario']
    mensaje = f'Hola {destinatario},\nEste es un correo de notificación para informarle sobre ...'
    enviar_correo(destinatario, mensaje)

print('Correos electrónicos enviados correctamente.')
