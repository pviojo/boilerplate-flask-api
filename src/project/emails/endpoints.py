import io
import re
import click
from datetime import datetime
from flask import Blueprint, jsonify, request, make_response, send_file
from .service import EmailService

emails_blueprint = Blueprint('emails', __name__)


@emails_blueprint.route('/emails/send', methods=['POST'])
def send() -> dict:
    data = request.json
    
    body = data.get('body', '')
    subject = data.get('subject', '')
    categories = data.get('categories', [])
    recipients = data.get('recipients', None)
    if not recipients:
        return {
            'msg': 'No recipients'
        }, 400
            

    is_real = data.get('real', False)
    if not is_real:
        recipients = list(set(filter(lambda x: re.search("@example.com", x), recipients)))
    
    rsp = EmailService.send({
        'body': body, 
        'categories': categories,
        'subject': '{prefix}{subject}'.format(
            prefix=
                'TEST - {d}'.format(d=datetime.utcnow().strftime('%Y-%m-%d %H:%i')) 
                if not is_real
                else '',
            subject=subject
        ),
        'to': [{'email': r} for r in recipients]
    })

    return {
        'rsp': rsp
    }, 200
    