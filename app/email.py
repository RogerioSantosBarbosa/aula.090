from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail
import requests
import json # Necessário para o SendGrid

def send_async_email(app, msg):
    with app.app_context():
        # Esta função é para SMTP (não usada na rota de API, mas mantida para compatibilidade)
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    
    # Renderiza o HTML do e-mail
    html_body = render_template(template + '.html', **kwargs)
    
    # Monta o cabeçalho de autenticação
    headers = {
        "Authorization": "Bearer " + app.config['API_KEY'],
        "Content-Type": "application/json"
    }
    
    # Monta o payload (corpo) da requisição no formato estrito do SendGrid
    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": to
                    }
                ],
                "subject": app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject
            }
        ],
        "from": {
            "email": app.config['API_FROM']
        },
        "content": [
            {
                "type": "text/html",
                "value": html_body
            }
        ]
    }

    # Envia a requisição POST para a API
    print(f'Tentando enviar e-mail via SendGrid para {to}...', flush=True)
    
    response = requests.post(
        app.config['API_URL'], 
        headers=headers, 
        json=data
    )
    
    # Log para ajudar no debug (aparecerá no console do PythonAnywhere)
    print(f'Status Code: {response.status_code}', flush=True)
    print(f'Resposta: {response.text}', flush=True)

    return response
