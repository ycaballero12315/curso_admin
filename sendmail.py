import json
import smtplib
from email.mime.text import MIMEText
from env.config import SMTP_CONFIG

# Función para enviar correo electrónico
def enviar_correo(destinatario, mensaje):
    # Agregar "@refcfg.cu" al destinatario y al usuario
    destinatario += "@refcfg.cu"
    usuario = SMTP_CONFIG['usuario'] + "@refcfg.cu"

    # Configurar servidor SMTP
    servidor_smtp = SMTP_CONFIG['servidor_smtp']
    puerto_smtp = SMTP_CONFIG['puerto_smtp']
    contraseña = SMTP_CONFIG['contrasenna']

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

def main():
    # Leer archivo JSON
    with open('./resources/propietario.json') as f:
        datos = json.load(f)

    # Iterar sobre los propietarios y enviar correo electrónico
    for propietario in datos:
        destinatario = propietario['propietario']
        mensaje = f'Hola {destinatario},\nEste es un correo de notificación para informarle sobre ...'
        enviar_correo(destinatario, mensaje)

    print('Correos electrónicos enviados correctamente.')

if __name__ == "__main__":
    main()


