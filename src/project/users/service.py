import urllib
import jwt
from datetime import datetime, timedelta
from flask import current_app as app
from project import db, bcrypt

from project.emails.service import EmailService

from .models import User, BlacklistToken, Relation


class UserService:

    @staticmethod
    def register(user: dict):
        if not 'email' in user or not 'password' in user:
            return {
                'status': 'error',
                'exception': 'Missing email or password'
            }

        u = UserService.get_by_email(email=user.get('email'))
        if u:
            return {
                'status': 'error',
                'exception': 'User already exists'
            }

        u = User(
            email=user.get('email'),
            password=user.get('password')
        )

        try:
            u.save()
            return {
                'status': 'ok',
                'user': u.json()
            }
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'exception': str(e)
            }

    @staticmethod
    def get_by_email(email: str):
        user = User.query.filter(User.email == email).first()
        return user

    @staticmethod
    def change_password(id: int, password: str):
        user = UserService.get_by_id(id)
        if not user:
            return None
        user.set_password(password)
        try:
            user.save()
            return UserService.login({
                'email': user.email, 
                'password': password
            })
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'exception': str(e)
            }
    
    @staticmethod
    def get_by_id(id: int):
        user = User.query.filter(User.id == id).first()
        return user
    
    @staticmethod
    def login(u: dict):
        
        if not 'email' in u or not 'password' in u:
            return {
                'status': 'error',
                'exception': 'Missing email or password'
            }
        password = u.get('password')
        email = u.get('email')
        user = UserService.get_by_email(email=email)
        if not user:
            return {
                'status': 'error',
                'exception': 'No user found'
            }
        if not bcrypt.check_password_hash(
                user.password, u.get('password')
            ):
            return {
                'status': 'error',
                'exception': 'Password mismatch'
            }

        token = UserService.encode_auth_token(user.json())
        if token:
            user = UserService.get_user_from_token(token)
            return {
                'status': 'ok',
                'token': token,
                'user': user
            }

        return {
            'status': 'error',
            'exception': 'No token generated'
        }

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        """
        try:
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return {
                    'status': 'error',
                    'msg': 'Token blacklisted'
                }
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms=['HS256'])
            return {
                'status': 'ok',
                'payload': payload
            }
        except jwt.ExpiredSignatureError:
            return {
                'status': 'error',
                'msg': 'Signature expired'
            }
            return
        except jwt.InvalidTokenError as e:
            return {
                'status': 'error',
                'msg': 'Invalid token',
                'e': e
            }

    """
    Generates the Auth Token
    :return: string
    """
    @staticmethod
    def encode_auth_token(u, days=5):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=days),
                'iat': datetime.utcnow(),
                'sub': u
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return False

    @staticmethod
    def get_user_from_token(token: str):
        rsp = UserService.decode_auth_token(token)
        if rsp and 'status' in rsp and rsp['status'] == 'ok' and 'payload' in rsp and 'sub' in rsp['payload']:
            return rsp['payload']['sub']
        return None

    @staticmethod
    def blacklist_token(token: str):
        t = BlacklistToken(
            token=token
        )
        t.save()

    @staticmethod
    def get_relations_user(user_id: int):
        relations = Relation.query.filter(
            Relation.user_id == user_id,
        ).all()
        return relations

    @staticmethod
    def forget_password(user: dict):
        if not 'email' in user:
            return {
                'status': 'error',
                'exception': 'Missing email or password'
            }
        user  = UserService.get_by_email(user.get('email'))
        if not user:
            return None
        token = token = UserService.encode_auth_token(user.json(), days=1)

        
        email = {
            'to':[{
                'email': user.email,
            }],
            'subject':'Cambia tu contraseña',
            'layout':'default',
            'categories': ['forget_password'],
            'body':'''
                <div class="inner">
                    <p>Hola,<p>
<p>Tu, o alguien más, ha solicitado cambiar la contraseña de esta cuenta de correo electrónico. Para continuar el proceso por favor haz click en el siguiente botón</p>
<br/>
<a href="{url}/{token}" class="button">Cambiar la contraseña</a>
<p><small>Si no has sido tu no te preocupes, no debes hacer nada. Tu cuenta está segura</small></p>
<br/>
                    Saludos,
                    <br/>
                    
                '''.format(
                    url='',
                    token=token,
                )

        }
        rsp = EmailService.send(email)
        return True
        

    


