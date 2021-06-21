from hashlib import md5
import random
import re
import string


def hash(s: str):
    return md5(
        bytes(
            '{}'.format(s), 'utf'
        )
    ).hexdigest()[0:32]


def hash_with_prefix(prefix: str, s: str = None):
    if not s:
        letters = string.ascii_lowercase
        s = ''.join(random.choice(letters) for i in range(20))

    s = md5(
        bytes(
            '{}'.format(s), 'utf'
        )
    ).hexdigest()
    
    return '{}-{}-{}-{}-{}-{}'.format(
        md5(
            bytes(
                '{}'.format(prefix), 'utf'
            )
        ).hexdigest()[0:4],
        s[0:4],
        s[4:8],
        s[8:12],
        s[12:16],
        s[16:20],
    )

def get_token(headers, params=None):
    if params and params.get('access_token'):
        return params.get('access_token')

    auth_token = None
    auth_header = headers.get('Authorization')
    if not auth_header:
        auth_header = headers.get('access-token')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    return auth_token
