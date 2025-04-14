
# myapp/authentication.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return None  # Sin encabezado, pasa al siguiente autenticador o da 401 si no hay otro

        if api_key != settings.APP_API_KEY:
            raise AuthenticationFailed('API Key inválida')

        return (None, None)  # Retorna un user anónimo o puedes retornar un usuario real
