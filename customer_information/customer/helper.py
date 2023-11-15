import jwt, base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as decryptionPadding
from cryptography.hazmat.backends import default_backend
from datetime import date as d, datetime as dt
import os

def NewAuthenticateJWTtoken(request):

    # Load your public RSA key
    with open('customer/key/_._.pharmacy_jwt_pass.click.pkcs8', 'rb') as public_key_file:
        public_key = serialization.load_pem_public_key(
            public_key_file.read(),
            backend=default_backend()
        )

    response = {"mobileNumber" : "", "isValid" : False }

    try:
        jwt_token = request.headers.get('authorization', None)
        jwt_token_bytes = base64.b64decode(jwt_token.encode('utf-8'))
        jwt_token = jwt_token_bytes.decode('utf-8')
    except:
        return response

    try:
        # payload = jwt.decode(jwt_token, JWT_SECRET,algorithms=[JWT_ALGORITHM])
        payload = jwt.decode(jwt_token, public_key, algorithms=['RS256'])
        response = {"mobileNumber": payload["mobileNumber"], "isValid" : True }
    except jwt.DecodeError:
        print(f"JWT Token Decode Error LOG : {str(jwt.DecodeError)}")
    except jwt.ExpiredSignatureError:
        print(f"JWT Token Expired Signature Error LOG : {str(jwt.ExpiredSignatureError)}")
    
    return response

def NewGetJwtToken(phone_number):
    
    # Load your private RSA key
    with open('customer/key/_._.pharmacy_jwt_pass.click.pkcs8', 'rb') as private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(),
            password = b"jwt123",
            backend = default_backend()
        )
    
    private_key_file.close()

    JWT_ALGORITHM = 'RS256'
    JWT_EXP_DELTA_DAYS = 7  # Set expiration to 7 days
    JWT_EXP_DELTA_SECONDS = JWT_EXP_DELTA_DAYS * 24 * 60 * 60
    JWT_EXP_DELTA_SECONDS_REFRESH = JWT_EXP_DELTA_DAYS * 24 * 60 * 60

    payload = {
        "mobileNumber": phone_number,
        "exp": dt.utcnow() + dt.timedelta(seconds=JWT_EXP_DELTA_SECONDS),
    }

    # Sign the access token using RS256
    jwt_token = jwt.encode(payload, private_key, algorithm=JWT_ALGORITHM)
    jwt_token = base64.b64encode(jwt_token.encode('utf-8')).decode('utf-8')
    jwt_token = str(jwt_token)

    payload_refreshToken = {
        "mobileNumber": phone_number,
        'exp': dt.utcnow() + dt.timedelta(seconds=JWT_EXP_DELTA_SECONDS_REFRESH),
    }

    # Sign the refresh token using RS256
    jwt_token_refresh = jwt.encode(payload_refreshToken, private_key, algorithm=JWT_ALGORITHM)
    jwt_token_refresh = base64.b64encode(jwt_token_refresh.encode('utf-8')).decode('utf-8')
    jwt_token_refresh = str(jwt_token_refresh)

    return { "token" : jwt_token, "refresh_token" : jwt_token_refresh }

