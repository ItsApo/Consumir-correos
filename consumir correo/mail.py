import imaplib
import email
from email.header import decode_header

# Configuración IMAP para Gmail
username = "cesdetest@gmail.com"
password = "mmshlmvqddltvfjs"
imap_server = "imap.gmail.com"
port = 993

try:
    # Conexión al servidor IMAP
    mail = imaplib.IMAP4_SSL(imap_server, port)
    mail.login(username, password)
    print("Conexión exitosa al servidor IMAP")

    # Seleccionar la bandeja de entrada
    mail.select("inbox")

    # Buscar mensajes en la bandeja de entrada
    status, email_ids = mail.search(None, "ALL")
    email_ids = email_ids[0].split()

    # Iterar a través de los mensajes
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        email_msg = email.message_from_bytes(msg_data[0][1])

        # Decodificar el asunto
        subject, encoding = decode_header(email_msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")


        # Mostrar información del mensaje
        print("-" * 50)
        print("Asunto:", subject)
        print("De:", email_msg["From"])
        print("Fecha:", email_msg["Date"])

        # Leer el cuerpo del mensaje (solo texto)
        if email_msg.is_multipart():
            for part in email_msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    print("Cuerpo del mensaje:")
                    print(body)

except imaplib.IMAP4.error as e:
    print("Error al conectar y autenticar con el servidor IMAP:", str(e))
except Exception as e:
    print("Ocurrió un error inesperado:", str(e))
finally:
    # Cerrar la conexión
    if "mail" in locals():
        mail.logout()