
import json
import os

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

