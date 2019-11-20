from jose import jwt
from django.conf import settings


class JwtHelper(object):
    """Jwt operations"""

    def decode_data(self, payload):
        """Decode data from server"""
        return jwt.decode(payload, settings.SECRET_KEY, algorithms=['HS256'])

    def encode_data(self, document):
        """Encode data for server """
        return jwt.encode(document, settings.SECRET_KEY, algorithm="HS256")
