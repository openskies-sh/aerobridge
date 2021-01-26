
import json
import os
from functools import wraps
from django.contrib.auth import authenticate
import jwt
import requests
from os import environ as env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from six.moves.urllib import request as req
from django.http import JsonResponse
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
import requests
from django.conf import settings

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
    
    decoded = jwt.decode(token, public_key, audience=audience, issuer=issuer, algorithms=['RS256'])
    return decoded



def requires_scopes(required_scopes):
    """Determines if the required scope is present in the access token
    Args:
        required_scopes (list): The scopes required to access the resource
    """
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):       
            if settings.SECURE_API_ENDPOINTS:
                request = args[0]
                auth = request.META.get("HTTP_AUTHORIZATION", None)
                
                if auth:
                    parts = auth.split()
                    token = parts[1]            
                else:             
                    response = JsonResponse({'detail': 'Authentication credentials were not provided'})
                    response.status_code = 401
                    return response

                PASSPORT_DOMAIN = 'https://{}/.well-known/jwks.json'.format(env.get('PASSPORT_DOMAIN'))
                API_IDENTIFIER = env.get('PASSPORT_AUDIENCE')
                
                jsonurl = req.urlopen(PASSPORT_DOMAIN)
                
                jwks = json.loads(jsonurl.read())   
                # cert = '-----BEGIN CERTIFICATE-----\n' + \
                    # jwks['keys'][0]['x5c'][0] + '\n-----END CERTIFICATE-----'
                # certificate = load_pem_x509_certificate(cert.encode('utf-8'), default_backend())
                # public_key = certificate.public_key()
                public_keys = {}
                for jwk in jwks['keys']:
                    kid = jwk['kid']
                    public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
                
                kid = jwt.get_unverified_header(token)['kid']
                public_key = public_keys[kid]
                try:
                    decoded = jwt.decode(token, public_key, audience=API_IDENTIFIER, algorithms=['RS256'])
                    
                except jwt.ExpiredSignatureError as es: 
                    response = JsonResponse({'detail': 'Token Signature has expired'})
                    response.status_code = 401
                    return response
                except jwt.InvalidAudienceError as es: 
                    response = JsonResponse({'detail': 'Invalid audience in token'})
                    response.status_code = 401
                    return response
                
                except jwt.InvalidIssuerError as es: 
                    response = JsonResponse({'detail': 'Invalid issuer for token'})
                    response.status_code = 401
                    return response

                except jwt.InvalidSignatureError as es: 
                    response = JsonResponse({'detail': 'Invalid signature in token'})
                    response.status_code = 401
                    return response
                except Exception as e: 
                    response = JsonResponse({'detail': 'Invalid token'})
                    response.status_code = 401
                    return response

                

                if decoded.get("scope"):
                    token_scopes = decoded["scope"].split()
                    token_scopes_set = set(token_scopes)                
                    if set(required_scopes).issubset(token_scopes_set):
                        return f(*args, **kwargs)
                response = JsonResponse({'message': 'You don\'t have access to this resource'})
                response.status_code = 403
                return response
            else:
                return f(*args, **kwargs)


        return decorated

    return require_scope


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r