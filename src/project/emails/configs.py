import os
basedir = os.path.abspath(os.path.dirname(__file__))

emails_providers_config = {
    'default': {
        'provider': 'sendgrid',
        'apikey': os.environ.get('SENDGRID_API_KEY', ''),
        'default_from': {
            "name": "Test",
            "email": "no-reply@mail.example.com"
        }
    }
}
