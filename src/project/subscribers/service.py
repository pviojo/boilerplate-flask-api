import urllib
from project import db

from .models import Subscriber
from project.common.helpers import hash_with_prefix
from ..emails.service import EmailService

class SubscriberService:

    @staticmethod
    def create(subscriber: dict):
        if not 'email' in subscriber:
            return {
                'status': 'error',
                'exception': 'Missing email'
            }

        existing_subscriber = SubscriberService.get_by_email(
            email = subscriber.get('email'),
        )

        if existing_subscriber:
             return {
                'status': 'error',
                'exception': 'Subscriber already exists'
            }

        s = Subscriber()
        s.email = subscriber.get('email', '').strip()
        s.name = subscriber.get('name', '')
        s.status = 'PENDING'


        s.hash = hash_with_prefix(
            prefix='subscriber',
            s='{}'.format(s.email)
        )

        try:
            s.save()
            SubscriberService.notify_creation(s.email, s.hash)
            return {
                'status': 'ok',
                'subscriber': s.json()
            }
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'exception': str(e)
            }

    @staticmethod
    def get_by_hash(hash: str):
        subscriber = Subscriber.query.filter(Subscriber.hash == hash).first()

        return subscriber

    @staticmethod
    def get_by_id(id: int):
        subscriber = Subscriber.query.filter(Subscriber.id == id).first()

    @staticmethod
    def get_by_email(email: str):
        subscriber = Subscriber.query.filter(Subscriber.email == email.strip()).first()
        return subscriber

    @staticmethod
    def get_by_email_and_hash(email: str, hash:str):
        subscriber = Subscriber.query.filter(Subscriber.email == email.strip(), Subscriber.hash == hash).first()
        return subscriber

    @staticmethod
    def notify_creation(email: str, hash: str):
        email = {
            'to':[{
                'email': email,
            }],
            'subject':'¡Confirma tu subscripción a {}!'.format('Test Flask'),
            'layout':'default',
            'params':{
                'footer_text':'Recibiste este mail porque tu o alguien más ha suscrito esta cuenta de correo electrónico a la tienda {}'.format('Test Flask'),
                'site_name': 'Test Flask',
            },
            'body':'''
            <div class="title">¡Confirma tu subscripción!</div>
            <div class="inner">
<p>Hola,<p>
<p>Tu o alguien más ha suscrito esta cuenta de correo electrónico a <strong>{site_name}</strong>. Para confirmar que eres tú, por favor haz click en el siguiente botón</p>
<br/>
<a href="{url}/confirm?{confirm_params}" class="button">¡Confirmar mi suscripción!</a>
<p><small>Si no has sido tu no te preocupes, no debes hacer nada y no recibiras emails en el futuro de esta tienda.</small></p>
        '''.format(
            confirm_params = urllib.parse.urlencode({'e': email, 'h': hash}),
            site_name='Test Flask',
            email=email,
            url='',
            hash=hash
        )

        }
        rsp = EmailService.send(email)
        return True

    @staticmethod
    def confirm(email: str,  hash: str):
        subscriber = SubscriberService.get_by_email_and_hash(email=email, hash=hash)

        if not subscriber:
            return False

        if subscriber.status != 'PENDING':
            return subscriber

        subscriber.status='CONFIRMED'
        subscriber.save()
        return subscriber

    @staticmethod
    def unsubscribe(email: str,  hash: str):
        subscriber = SubscriberService.get_by_email_and_hash(email=email, hash=hash)

        if not subscriber:
            return False

        if subscriber.status == 'UNSUBSCRIBED':
            return subscriber

        subscriber.status='UNSUBSCRIBED'
        subscriber.save()
        return subscriber

    @staticmethod
    def get(filter_status: list=None):
        subscribers = Subscriber.query.filter()
        if filter_status and len(filter_status)>0:
            subscribers = subscribers.filter(Subscriber.status.in_(filter_status))
        subscribers = subscribers.all()
        return subscribers
