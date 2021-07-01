from flask import Flask, Response, request, jsonify
from .configs import emails_providers_config
from .providers.sendgrid import SendgridProvider
from .layout import Layout

class EmailService:
    @staticmethod
    def send(email):
        Flask(__name__, template_folder='layouts')

        if 'config' not in email:
            email['config'] = 'default'

        if not email['config'] in emails_providers_config:
            return {
                'message':'Config not found',
                'status':'error'
            }

        config = emails_providers_config.get(email.get('config'))

        if 'from' not in email:
            email['from'] = config.get('default_from')


        html = email.get('body')
        if 'layout' in email:
            params = email.get('params', None)

            html = Layout.process(
                template=email.get('layout'),
                body=html,
                params=params)
    

        if 'layout_params' in email:
            for k, v in email.get('layout_params').items():
                html = html.replace('%%param.' + k + '%%', v)

        if 'categories' not in email:
            email['categories'] = []

        email['categories'].append("test-flask-api")

        if config.get('provider') == 'sendgrid':
            provider = SendgridProvider(config)
        else:
            return {
                'message':'Provider {} not found'.format(config.get('provider')),
                'status':'error'
            }

        responses = []
        for recipient in email.get('to'):
            data = {
                'from': email.get('from'),
                'to': recipient,
                'subject': email.get('subject'),
                'html': html,
                'categories': email.get('categories'),
            }
            r = provider.send(data)
            responses.append(r)

        return {
            'message':'OK',
            'status':'ok',
            'responses': responses
        }
