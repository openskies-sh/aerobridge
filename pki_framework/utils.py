
import json
import os
from functools import wraps
from django.contrib.auth import authenticate
import jwt
import requests
from os import environ as env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())



def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    passport_url = 'https://{}/.well-known/jwks.json'.format(env.get('PASSPORT_DOMAIN'))
   
    jwks = requests.get(passport_url).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format(env.get('PASSPORT_DOMAIN'))
    audience = env.get('PASSPORT_AUDIENCE')
    print(audience)
    decoded = jwt.decode(token, public_key, audience=audience, issuer=issuer, algorithms=['RS256'])
    return decoded


def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token

def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope

