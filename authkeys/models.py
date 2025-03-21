from django.db import models

from rest_framework_api_key.models import AbstractAPIKey

class ServiceAPIKey(AbstractAPIKey):
    """
    API Keys específicas para autenticación en servicios externos.
    """
    class Meta:
        verbose_name = "API Key para Servicios"
        verbose_name_plural = "API Keys para Servicios"
